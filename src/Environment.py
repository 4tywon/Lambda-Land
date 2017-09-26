# Untested
class Environment:
    def __init__(self, parent):
        self.vars = None
        self.ownvars = dict()
        if parent != None:
            self.vars = parent.vars
        self.parent = parent
    def extend(self):
        return Environment(self)
    def lookup(self, name):
        scope = self
        while scope != None:
            if name in scope.ownvars:
                return scope
            scope = scope.parent
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        print("Undefined variable " + name)
    def set(self, name, value):
        scope = self.lookup(name)
        if (scope == None and self.parent):
            print("Undefined variable " + name)
        (scope or self).vars[name] = value
        return value
    def define(self, name, value):
        self.vars[name] = value
        self.ownvars[name] = value
        return value
    
