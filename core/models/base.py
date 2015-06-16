import core.managers.base_manager as base_manager

managers = base_manager.ManagerSelector()


class ModelValidationError(Exception):
    """Thrown when model validation fails."""
    pass


class RequiredFieldError(ModelValidationError):
    """Thrown when a model is missing a required field."""
    pass

class ModelBaseType(type):
    """Meta-class for Model."""

    def __new__(cls, name, bases, attrs):
        """Sets up the new model so we can set the model on the manager."""
        new_cls = super(ModelBaseType, cls).__new__(cls, name, bases, attrs)
        new_cls._model_fields = {}
        for obj_name, obj in attrs.items():
            new_cls.add_to_class(obj_name, obj)

        return new_cls

    def add_to_class(cls, obj_name, obj):
        """Set object as an attribute on the model.

        Some attributes want to more closely hook into models
        To do so they need to implement hook_into_model
        This gives them access to the model
        """
        if hasattr(obj, 'hook_into_model'):
            obj.hook_into_model(cls, obj_name)
        else:
            setattr(cls, obj_name, obj)

class Model(object):
    __metaclass__ = ModelBaseType

    
    def _set_attributes(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("takes at most 1 argument (%d given)" %
                                len(args))
            kwargs.update(dict(args[0]))

        for key, val in kwargs.iteritems():
            try:
                key = str(key)
            except UnicodeError:
                pass
            
            try:
                setattr(self, key, val)
            except AttributeError:
                continue

    def __init__(self, *args, **kwargs):
        self._data = self._get_data()
        self._set_attributes(*args, **kwargs)

    def __contains__(self, key):
        return key in self._data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def pop(self, key, *args):
        self.modified = self.modified or key in self._data
        return self._data.pop(key, *args)

    def update(self, dict_):
        self._data.update(dict_)

    def values(self):
        return self._data.values()

    def iterkeys(self):
        return self._data.iterkeys()

    def itervalues(self):
        return self._data.itervalues()

    def iteritems(self):
        return self._data.iteritems()

    def clear(self):
        self._data_cache = {}

    def _get_data(self, no_load=False):
        """
        Lazily loads data from storage (unless "no_load" is True, when only
        an empty dict is stored) and stores it in the current instance.
        """
        try:
            return self._data_cache
        except AttributeError:
            self._data_cache = dict()
        return self._data_cache

    @classmethod
    def unmutable_fields(cls):
        return ['id']
