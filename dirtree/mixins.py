import pprint

from .utils import identity


class FieldsMixin:
    def _iter_repr_fields(self, _repr=repr):
        for field in self.__repr_fields__:
            if isinstance(field, tuple):
                field, f = field
            else:
                field, f = field, _repr

            value = getattr(self, field)
            value = f(value)

            yield field, value

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__, ', '.join(map('='.join, self._iter_repr_fields())))


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


def _format_kwargs(self, items, stream, indent, allowance, context, level):
    write = stream.write
    indent += self._indent_per_level
    delimnl = ',\n' + ' ' * indent
    last_index = len(items) - 1
    for i, (key, ent) in enumerate(items):
        last = i == last_index
        rep = str(key)
        write(rep)
        write('=')
        self._format(ent, stream, indent + len(rep) + 1,
                     allowance if last else 1, context, level)
        if not last:
            write(delimnl)


def _pprint_fields_mixin(self, object, stream, indent, allowance, context, level):
    cls = object.__class__
    stream.write(cls.__name__ + '(')
    _format_kwargs(
        self,
        list(object._iter_repr_fields(identity)),
        stream,
        indent + len(cls.__name__),
        allowance + 1,
        context,
        level
    )
    stream.write(')')


pprint.PrettyPrinter._dispatch[FieldsMixin.__repr__] = _pprint_fields_mixin
