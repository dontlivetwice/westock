

def memoized_property(prop):
    """Memoizes the results of the property.

    Args:
        prop: A function that will become the property and have its
            results memoized.

    Returns:
        Memoized property function.

    """
    attribute_name = "__%s" % prop.__name__

    def get_fn(self):
        if not hasattr(self, attribute_name):
            setattr(self, attribute_name, prop(self))

        return getattr(self, attribute_name)

    def set_fn(self, value):
        setattr(self, attribute_name, value)

    def del_fn(self):
        delattr(self, attribute_name)

    return property(fget=get_fn, fset=set_fn, fdel=del_fn, doc=prop.__doc__)
