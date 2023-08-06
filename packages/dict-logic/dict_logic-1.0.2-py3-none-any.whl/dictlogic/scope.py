from contextlib import contextmanager


scopes = []

class Scope:
    def __init__(self, globals=None):
        from .builtins import namespace as builtins
        self.builtins = builtins
        self.globals = globals if globals is not None else {}
        self.locals = {}

    def find(self, name):
        for namespace in self.namespaces():
            if name in namespace:
                return namespace
        return None

    def resolve(self, name):
        namespace = self.find(name)
        if namespace is None:
            return None
        return namespace[name]

    def namespaces(self, with_builtins=True):
        yield self.locals
        yield self.globals
        if with_builtins:
            yield self.builtins


def push_scope(globals):
    scopes.append(Scope(globals))

def pop_scope():
    scopes.pop()

def current_scope():
    return scopes[-1]

@contextmanager
def create_scope(globals):
    push_scope(globals)
    yield current_scope()
    pop_scope()