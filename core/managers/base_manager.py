import MySQLdb
import types
from core.managers.db_manager import DBManager


class ManagerException(Exception):
    pass


class Manager(object):
    def __init__(self, db_name):
        self.db_manager = DBManager(db_name)

    @classmethod
    def _serialize(cls, obj):
        """ Serializes the passed in object """
        raise NotImplementedError

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object """
        raise NotImplementedError

    @classmethod
    def _derive_key(cls, prefix, key):
        return "%s:%s" % (prefix, key)

    def add_one(self, obj):
        """ Adds the passed in object to the DB
            sub classes should implement this """
        raise NotImplementedError

    def update_one(self, obj):
        """ Updates the passed in object in the DB"""
        if obj:
            query = " "

            serialized_obj = self._serialize(obj)

            count = 1

            for value in serialized_obj:
                if obj.__class__.DB_MAPPINGS[count] not in obj.__class__.unmutable_fields():
                    if value is not None:

                        if isinstance(value, unicode) or isinstance(value, str):
                            value = MySQLdb.escape_string(value)

                        query += '%s = \'%s\', ' % (obj.__class__.DB_MAPPINGS[count], value)

                count += 1

            query = query[:-2] + ''' WHERE id=%s''' % obj.get('id')

            return self.db_manager.update_one(query)

        raise ManagerException('%sIsNoneError' % obj.__class__)

    def get_one(self, **kwargs):
        """ Gets the passed in object from the DB"""
        query = ""

        for key, value in kwargs.items():
            if isinstance(value, unicode) or isinstance(value, str):
                value = MySQLdb.escape_string(value)

            query += '%s = \"%s\" AND ' % (key, value)

        query = query[:-5]

        obj = self.db_manager.get_one(query)

        return self._deserialize(obj)

    def delete_one(self, obj):
        """ Deletes the passed in object from the DB"""
        if obj:
            query = 'id = \"%s\"' % obj.get('id')

            return self.db_manager.delete_one(query)

        raise ManagerException('%sIsNoneError' % obj.__class__)

    def get_many(self, limit=None):
        objs = self.db_manager.get_many(limit)

        deserialized_objs = []

        if objs:
            for obj in objs:
                deserialized_objs.append(self._deserialize(obj))

        return deserialized_objs


class ManagerSelector(object):
    """Allows for managers to be registered with a group name and then set.

    Once a manager has been used, that group is set for this initialization of
    the manager selector.

    Managers take arbitrary keyword parameters for initialization passed in when
    the group is set. If a manager does not use these keyword initialization
    parameters, its __init__ function should ignore them.
    """

    _manager_types = (
        "db_manager",
        "stock_manager",
        "user_manager",
        "interest_manager",
        "user_stock_manager"
    )

    def __init__(self, **kwargs):    	
        self.manager_groups = {}
        self.initialized = False
        for group, managers in kwargs.iteritems():
            self.manager_groups[group] = managers

        for manager in self._manager_types:
            def manager_attr_gen(manager):
                def manager_attr(self):
                    if not self.initialized:
                        self.initialized = True
                    return self.__dict__['%s' % manager]
                return manager_attr
            self.__dict__[manager] = types.MethodType(manager_attr_gen(manager), self)

    def register(self, group, managers):
        self.manager_groups[group] = managers

    def _set_manager(self, manager_group, manager_type, **kwargs):
        try:
            manager = self.manager_groups[manager_group][manager_type]
            self.__dict__['%s' % manager_type] = manager(**kwargs)
        except KeyError:
            pass

    def set_group(self, manager_group, **kwargs):
        if self.initialized:
            raise Exception("Manager selector cannot be reset after it has been initialized.")

        for key in self._manager_types:
            self._set_manager(manager_group, key, **kwargs)