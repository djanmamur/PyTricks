from re import compile as compile_regex_pattern


class Descriptor(object):
    """
    Desciptor metaclass for get, set and delete of the values.
    """

    __slots__ = ("name",)

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name in instance.__dict__:
            raise ValueError(
                "Value Error in <{cls}>: instance `{instance}` already contains value with key `{key}`.".format(
                    cls=instance.__class__.__name__, instance=instance, key=self.name
                )
            )
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

        else:
            raise ValueError(
                "Value Error in <{cls}>: cannot delete value `{key}` for instance of `{instance}`.".format(
                    cls=instance.__class__.__name__, instance=instance, key=self.name
                )
            )


class TypeCheckMixin(Descriptor):
    objectType = object

    def __set__(self, instance, value):
        if not isinstance(value, TypeCheckMixin.objectType):
            raise TypeError("Expect type {name}.".format(name=TypeCheckMixin.objectType))
        super().__set__(instance, value)


class Sized(Descriptor):
    """
    Create a Sized variable.
    This can be used
    to create a mixin of Typed Variables.
    """

    def __init__(self, *args, max_length: int, **kwds):
        self.max_length: int = max_length
        super(Sized, self).__init__(*args, **kwds)

    def __set__(self, instance, value):
        if len(value) > self.max_length:
            raise ValueError(
                "Validation Error in <{cls}>: Cannot set `{value}` for `{instance}`".format(
                    cls=instance.__class__.__name__, value=value, instance=instance
                )
            )

        super().__set__(instance, value)


class Regex(Descriptor):
    """"""

    def __init__(self, *args, pattern, **kwds):
        self.pattern = compile_regex_pattern(pattern)
        super().__init__(*args, **kwds)

    def __set__(self, instance, value):
        if not self.pattern.match(value):
            raise ValueError(
                "Value Error in <{cls}>: Cannot set value. Value `{value}` does not match pattern `{pattern}`".format(
                    cls=instance.__class__.__name__, value=value, pattern=self.pattern
                )
            )
        super().__set__(instance, value)


class Integer(TypeCheckMixin):
    objectType = int


class Float(TypeCheckMixin):
    objectType = float


class String(TypeCheckMixin):
    objectType = str


class SizedInteger(Integer, Sized):
    pass


class SizedFloat(Float, Sized):
    pass


class SizedString(String, Sized):
    pass


class SizedRegexString(SizedString, Regex):
    pass
