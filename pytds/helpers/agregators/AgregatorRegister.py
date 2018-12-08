class AgregatorRegister(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        """ @param name: Name of the class
            @param bases: Base classes (tuple)
            @param attrs: Attributes defined for the class
        """
        new_cls = super(AgregatorRegister, cls).__new__(cls, name, bases, attrs)
        cls.REGISTRY[name] = new_cls
        return new_cls
