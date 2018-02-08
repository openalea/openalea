
from code import InteractiveInterpreter


class Interpreter(InteractiveInterpreter):

    @property
    def user_ns(self):
        return self.locals

    @user_ns.setter
    def user_ns(self, ns):
        self.locals = ns

    def run_cell(self, raw_cell, **kwargs):
        return self.runcode(raw_cell)

    def run_code(self, code_obj):
        return self.runcode(code_obj)

    def reset(self, namespace=None, **kwargs):
        self.locals.clear()
        if namespace:
            self.locals.update(namespace)

    def update(self, namespace, **kwargs):
        namespace.update(self.locals)

    def push(self, variables, **kwargs):
        self.locals.update(variables)

    def get(self, varnames, **kwargs):
        dic = {}
        for name in varnames:
            dic[name] = self.locals[name]
        return dic

    def delete(self, varnames, **kwargs):
        for name in varnames:
            del self.locals[name]
