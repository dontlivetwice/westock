# Copyright (c) 2012, Pinterest Inc.  All rights reserved.

"""Utilities to process objects with fields."""

import copy

from dictshield import fields as shieldfields
from dictshield.base import ShieldException
from flufl.enum import Enum
from flufl.enum import IntEnum

from utils.email import VALID_EMAIL
from core.models.base import Model
from core.models.base import ModelValidationError
from core.models.base import RequiredFieldError

class FieldValidationError(Exception):
    """An error representing a field validation issue."""

    def __init__(self, message, field_class=None, field_name=None, value=None):
        self._message = message
        self._field_class = field_class
        self._field_name = field_name
        self._value = value

    def __str__(self):
        return self._message

    @property
    def detailed_message(self):
        detailed = self._message
        field_class = self._field_class or ""
        field_name = self._field_name or ""
        value = self._value or ""
        return "%s(%s): %s[%s]" % (field_class, field_name, value, detailed)

    @property
    def message(self):
        return self.detailed_message


class RequiredFieldValidationError(FieldValidationError):
    """An error representing a require field failing."""
    pass


class Field(object):
    """A base field class.

    It has basic field processing functions such as ``set``, ``get``,
    ``to_python``, ``to_json``.
    """

    def __init__(self, null=True, default=None, required=False,
                 name=None, include_in_cache=True, conversion=None):
        """Constructor.

        Args:
            ``null``: A boolean to indicate whether the field is null.
            ``default``: A default value of the field.
            ``name``: Field name to store in the database.
            ``required``: A boolean indicating whether this field is required or not.
            ``include_in_cache``: True if the field should be cached with the
                model dictionary.  If set to False, the field will be filtered
                out of the dictionary before setting the object in memcache.
            ``conversion``: A callable that is applied to the value before it is returned.

        """
        self.field_name = name
        self.null = null
        self.default_value = default
        self._model_instance = None
        self.include_in_cache = include_in_cache
        self.required = required
        self.conversion = conversion if callable(conversion) else None

    def _default(self):
        return None

    @property
    def default(self):
        """Get the default value of the field.

        Over time we added multiple ways to set default values for the field.
        Here is how they are prioritized:
        - default in __init__ unless it is None
        - default defined in subclass in _default() function (unless it
          is None)
        - default defined in get() function in Model, if defined, not None
        - None value

        Returns:
            default value of the field.
        """
        default_val = None
        if callable(self.default_value):
            default_val = self.default_value()
        else:
            # Copy to reduce possibilities of modifying the default value.
            default_val = copy.copy(self.default_value)
        if default_val is not None:
            return default_val

        return self._default()

    def hook_into_model(self, model, field_name):
        """Hook the field together with a model.

        Args:
            ``model``: Data model, such as user_model, board_model etc.
            ```field_name``: The name of the field inside the ``model``.
        """

        self.model = model
        if self.field_name is None:
            self.field_name = field_name

        model._model_fields[self.field_name] = self
        setattr(model, self.field_name, self)

    def __set__(self, instance, value):
        """Set a field to an ``instance``.

        Args:
            ``instance``: An object we are setting the field to.

        Raises:
            AttributeError if instance is None or the field is null.
        """

        # TODO: If we get rid of Model being a dict
        # we will want to do instance.__dict__
        # or hide a dict on there
        if value is None and self.null is False:
            raise AttributeError('%s cannot be a null value.' %
                                 self.field_name)

        instance._data[self.field_name] = self.to_python(value)
        instance._dirty_fields.add(self.field_name)

    def __get__(self, instance, cls):
        """Get a field from an instance.

        Args:
            ``instance``: An object we are geting the field from.

        Returns:
            The field value from the ``instance``.

        Raises:
            AttributeError if instance is None or the instance doesn't
            have such a field.
        """
        if instance is None:
            raise AttributeError('Must be an instance of %s' % cls.__name__)

        value = None
        # Handle the case where we don't already have a value for this field.
        if self.field_name not in instance._data:
            instance._data[self.field_name] = self.default
            value = instance._data[self.field_name]
        else:
            # Get the field's value.  This is guaranteed to be set at this point.
            value = instance._data[self.field_name]

        # If we have a conversion callable, apply it to the value.
        if self.conversion is not None and value is not None:
            value = self.conversion(value)

        return value

    def to_python(self, value):
        """Parse a field to a Python object.

        Override this method to do custom casting.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A datetime value.
        """
        return value

    def to_json(self, value):
        """Serialize object to an object that can be json encoded.

        Override this method to do custom serialization.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A json object.
        """
        return value

    def validate(self, value, cleanse=False, **kwargs):
        try:
            self._validate(value)
        except Exception as e:
            if cleanse and self._model_instance:
                self._model_instance.delete_field(self.field_name)
            message = unicode(e)
            raise FieldValidationError(
                message, self.__class__.__name__, self.field_name, value)

    def _validate(self, value):
        pass

    def is_empty(self, value):
        """Default implementation, true if value is None and default value
        is None.
        """
        return value is None and self.default is None

    def set_model(self, model):
        self._model_instance = model


class StringField(Field):
    """A string type field."""

    def __init__(self, choices=None, *args, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        if choices is not None and not choices:
            raise ValueError("'choices' should not be empty")
        self.choices = choices

    def _validate(self, value):
        if self.choices is not None and value not in self.choices:
            raise ShieldException('Must be one of %s' % str(self.choices),
                                  self.field_name, value)
        shieldfields.StringField().validate(value)


class DateTimeField(Field):
    """A DateTime type field."""

    def to_python(self, value):
        """Parse a field to a datetime object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A datetime value.
        """
        if self.null and not value:
            return None

        return DateTimeProxy(value)

    def to_json(self, value):
        """Serialize the objec to json object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A json object.
        """
        if value is None:
            return ''
        return value.isoformat()

    def _validate(self, value):
        if isinstance(value, DateTimeProxy):
            shieldfields.DateTimeField().validate(value.datetime_target)
        else:
            shieldfields.DateTimeField().validate(value)


class IntField(Field):
    """An int type field."""

    def __init__(self, choices=None, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)
        if choices is not None and not choices:
            raise ValueError("'choices' should not be empty")
        self.choices = choices

    def to_python(self, value):
        """Parse a field to an int object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            An int value.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def _validate(self, value):
        if self.choices is not None and value not in self.choices:
            raise ShieldException('Must be one of %s' % str(self.choices),
                                  self.field_name, value)
        shieldfields.IntField().validate(value)


class EnumField(Field):
    """A field that holds an enumerated value."""

    def __init__(self, enum, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        if not issubclass(enum, Enum):
            raise TypeError('%r must inherit from flufl.enum.Enum' % enum)
        self.enum = enum

    def to_python(self, value):
        if value is not None:

            if issubclass(self.enum, IntEnum):
                value = int(value)

            return self.enum[value]

    def to_json(self, value):
        if value is not None:
            return value.value

    def _validate(self, value):
        if value not in self.enum:
            raise ShieldException('Must be one of %s' % self.enum,
                                  self.field_name, value)


class ThriftEnumField(Field):
    """A field that holds a value defined by a Thrift Enum.
    The values should be integers."""
    def __init__(self, thrift_enum, *args, **kwargs):
        super(ThriftEnumField, self).__init__(*args, **kwargs)
        if not issubclass(thrift_enum, TBase):
            raise TypeError('%r must inherit from TBase' % thrift_enum)
        elif not hasattr(thrift_enum, '_VALUES_TO_NAMES'):
            raise TypeError('%r must be an Enum with _VALUES_TO_NAMES attribute' % thrift_enum)
        self.thrift_enum = thrift_enum

    def _validate(self, value):
        if value not in self.thrift_enum._VALUES_TO_NAMES:
            raise ShieldException('Must be one of %s' % self.thrift_enum,
                                  self.field_name, value)


class TimestampField(Field):
    """A TimeStamp type field."""
    pass


class FloatField(Field):
    """A float type field."""

    def __init__(self, min=None, max=None, *args, **kwargs):
        super(FloatField, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def to_python(self, value):
        """Parse a field to a float object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A float value.
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            # TODO: is this correct? should we return 0.0?
            return value

    def _validate(self, value):
        field = shieldfields.FloatField(min_value=self.min, max_value=self.max)
        field.validate(value)


class IDField(IntField):
    """An ID field."""
    pass


class BooleanField(Field):
    """A boolean type field."""

    def to_python(self, value):
        """Parse a field to a boolean object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A boolean value.
        """
        return bool(value)

    def _validate(self, value):
        shieldfields.BooleanField().validate(value)


class NullableBooleanField(Field):
    """A tri-state boolean field support True/False/None.
    Use this field when you want to support None for boolean type
    data, otherwise use BooleanField directly.
    """

    def to_python(self, value):
        """Parse a field to a boolean object.

        Args:
            ``value``: A value to be parsed.

        Returns:
            A boolean value or none.
        """
        if value is None:
            return None
        return bool(value)

    def _validate(self, value):
        if value is not None:
            shieldfields.BooleanField().validate(value)


class EmailField(Field):
    """An email field."""

    def _validate(self, value):
        if not VALID_EMAIL.match(value):
            raise ShieldException('Invalid email address', self.field_name,
                                  value)
        return value


class MutableTypeField(Field):
    """A base class for fields whose base type is stateful"""

    def __get__(self, instance, owner):
        """This is a little hack to avoid actually tracking a mutable field
        being dirty. Ideally, we'd return some proxy object that monitors
        changes to its underlying watched object, but this is surprisingly
        difficult to do transparently in Python.
        """
        instance._dirty_fields.add(self.field_name)
        return super(MutableTypeField, self).__get__(instance, owner)


class ListField(MutableTypeField):
    """A list type field."""

    def __init__(self, field=None, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
        self._field = field

    def _default(self):
        """Default of ListField is an empty list.

        Returns:
            An empty list.
        """
        return list()

    def to_json(self, value):
        """Convers the ListField to a json serializable object.  If the
        ListField has a provided field type, convert each of the field
        items to json as well.
        """
        json_value = value
        if self._field and isinstance(value, list):
            json_value = [self._field.to_json(item) for item in value]
        return json_value

    def to_python(self, value):
        """Converts the ListField to a Python object.  If the ListField
        has a provided field type, convert each of those to Python.
        """
        if self._field and isinstance(value, list):
            return [self._field.to_python(item) for item in value]
        else:
            return value

    def validate(self, value, cleanse=False, **kwargs):
        """Validate a list object (``value``).  Will also validate that all
        values within the list are of a valid field type if ``field`` was
        specified on the object. ``FieldValidataionError`` will be thrown if
        validation fails.

        Args:
            ``cleanse``: when set to True, the validation will remove all
                invalid fields from the list object.  A ``FieldValidationError``
                will still be thrown if there were any invalid fields.
        """
        validated_values = []
        validation_error = None
        if not isinstance(value, list):
            validation_error = "Invalid list field: %s " % value
        if self._field:
            # If a validation field is provided, go through each item in the
            # list and validate it.
            for item in value:
                try:
                    self._field.validate(item, cleanse=cleanse, **kwargs)
                    validated_values.append(item)
                except Exception as e:
                    if not isinstance(e, RequiredFieldValidationError):
                        validated_values.append(item)
                    message = unicode(e)
                    validation_error = "List contains invalid values: %s" % message

        if validation_error:
            if cleanse and self._model_instance:
                if validated_values:
                    self._model_instance.set_field(self.field_name, validated_values)
                else:
                    self._model_instance.delete_field(self.field_name)
            raise FieldValidationError(
                validation_error, self.__class__.__name__, self.field_name,
                unicode(value))


class SortOrderField(IntField):
    """An integer type field, for use in conjunction with SortedListField,
    that represents a sort ordering. Indexing starts at zero (0)."""

    UNKNOWN_ORDER = -1

    def __init__(self, *args, **kwargs):
        kwargs['default'] = SortOrderField.UNKNOWN_ORDER
        super(SortOrderField, self).__init__(*args, **kwargs)


class SortedListField(ListField):
    """A list field that maintains sort order of the list."""
    def __init__(self, sort_field=None, **kwargs):
        super(SortedListField, self).__init__(**kwargs)
        self._sort_field = sort_field

    def to_python(self, value):
        list_value = super(SortedListField, self).to_python(value)
        if list_value and isinstance(list_value, list):
            self._sort_list(list_value)
        return list_value

    def _sort_list(self, list_value):
        if not self._sort_field:
            return

        sort_func = lambda x: getattr(x, self._sort_field, SortOrderField.UNKNOWN_ORDER)
        has_sort_order = lambda x: sort_func(x) != SortOrderField.UNKNOWN_ORDER
        if any(has_sort_order(x) for x in list_value):
            # Sort the list.
            list_value.sort(key=sort_func)
        else:
            # List elements have no sort order yet, so add it now. At
            # this point we have to assume _sort_field references a
            # SortOrderField.
            for order, value in enumerate(list_value):
                setattr(value, self._sort_field, order)


class DictField(MutableTypeField):
    """A dict type field."""

    def __init__(self, field=None, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)
        self._field = field

    def _default(self):
        return dict()

    def _validate(self, value, **kwargs):
        shieldfields.DictField().validate(value)

        if not isinstance(value, dict):
            validation_error = "Invalid dict field: %s " % value
            raise FieldValidationError(
                validation_error, self.__class__.__name__, self.field_name,
                unicode(value))
        if not self._field:
            return
        # If a validation field is provided, go through each item in the
        # dict and validate it.
        for field in value.itervalues():
            try:
                self._field.validate(field, **kwargs)
            except Exception as e:
                message = unicode(e)
                validation_error = "Dict contains invalid values: %s" % message
                raise FieldValidationError(
                    validation_error, self.__class__.__name__, self.field_name,
                    unicode(value))


class URLField(StringField):
    """A URL field."""
    def _validate(self, value):
        shieldfields.URLField().validate(value)


class SchemeAgnosticURLField(StringField):
    def _validate(self, value):
        if url_utils.is_valid_url(value):
            return value

        raise ShieldException("Invalid URL", self.field_name, value)


class ModelField(MutableTypeField):
    """A Pinterest data model field."""
    def __init__(self, model=None, *args, **kwargs):
        super(ModelField, self).__init__(*args, **kwargs)
        if not model:
            raise ValueError("A ModelField requires a model.")
        self._model_class = model

    def to_json(self, value):
        return value.to_json() if value is not None else None

    def to_python(self, value):
        return self._model_class(value) if value is not None else None

    def validate(self, model, cleanse=False, **kwargs):
        """Validate a ``model`` object.  A ``FieldValidationError`` will be
        thrown if validation fails.  If required fields are missing a
        ``RequiredFieldValidationError`` will be thrown.

        Args:
            ``cleanse``: when set to True, the validation will remove all
                invalid fields from the model object.  A ``FieldValidationError``
                will still be thrown if there were any invalid fields.
            ``required_fields``: True by default. When set to False, validation
                will ignore the required fields check.  This should generally be used
                for testing only.
        """
        required_field_failure = False
        failure_message = None
        if not isinstance(model, Model):
            failure_message = "Invalid model field."
        try:
            model.validate(cleanse=cleanse, **kwargs)
        except ModelValidationError as e:
            if isinstance(e, RequiredFieldError):
                required_field_failure = True
            failure_message = unicode(e)

        if failure_message:
            args = (failure_message, self.__class__.__name__, self.field_name,
                    unicode(model))
            # If the model is missing a required field, delete it during cleanse.
            if required_field_failure:
                if cleanse and self._model_instance:
                    self._model_instance.delete_field(self.field_name)
                raise RequiredFieldValidationError(*args)
            raise FieldValidationError(*args)
