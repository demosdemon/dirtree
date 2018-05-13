class FieldsMixin:
    def __iter_repr_fields(self):
        for field in self.__repr_fields__:
            if isinstance(field, tuple):
                field, _repr = field
            else:
                field, _repr = field, repr

            value = getattr(self, field)
            value = _repr(value)

            yield '='.join((field, value))

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join(self.__iter_repr_fields()))


class ValidateMixin:
    def validate(self):
        attrs = (attr for attr in dir(self) if not attr.startswith('_'))
        for attr in attrs:
            try:
                method = getattr(self, '_validate_%s' % attr)
            except AttributeError:
                pass
            else:
                value = getattr(self, attr)
                if value is not None:
                    try:
                        method(value)
                    except TypeError:
                        # method doesn't accept a parameter
                        method()
