import types

class ManagerException(Exception):
	pass


class Manager(object):
    def __init__(self, **kwargs):
        pass

	def login(self, username_or_email, password):
		pass

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
        "user_manager"
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