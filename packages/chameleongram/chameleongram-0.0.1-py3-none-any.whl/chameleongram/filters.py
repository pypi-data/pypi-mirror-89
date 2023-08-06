class _flt:
    def __add__(self, other):
        return _and(self, other)

    def __or__(self, other):
        return _or(self, other)

    def __invert__(self):
        return _not(self)

    def __call__(self, update, client: "chameleongram.Client" = None):
        try:
            return self.func(update)
        except TypeError:
            return self.func(update, client)

    __radd__ = __and__ = __add__
    # __call__ = check


class _not(_flt):
    def __init__(self, flt):
        self.flt = flt

    def __call__(self, update, client: "chameleongram.Client" = None):
        return not (self.flt(update, client) if client else self.flt(update))


class _and(_flt):
    def __init__(self, flt, other):
        self.flt = flt
        self.other = other

    def __call__(self, update, client: "chameleongram.Client" = None):
        return (
            (self.flt(update, client) and self.other(update, client))
            if client
            else (self.flt(update) and self.other(update))
        )


class _or(_flt):
    def __init__(self, flt, other):
        self.flt = flt
        self.other = other

    def __call__(self, update, client: "chameleongram.Client" = None):
        return (
            (self.flt(update, client) or self.other(update, client))
            if client
            else (self.flt(update) or self.other(update))
        )


class Filters:
    __and__ = lambda *_: ...
    __or__ = lambda *_: ...
    __invert__ = lambda *_: ...

    def create(func, client: "chameleongram.Client" = None):
        return type(
            "filter",
            (_flt,),
            {
                "func": (lambda self, update, client: func(client, update))
                if client is not None
                else (lambda self, update: func(update)),
                "__add__": _flt.__add__,
            },
        )()

    # private = create(lambda msg: msg.chat.type == "private")
    # group = create(lambda msg: msg.chat.type in ["group", "supergroup"])
    # channel = create(lambda msg: msg.chat.type == "channel")
