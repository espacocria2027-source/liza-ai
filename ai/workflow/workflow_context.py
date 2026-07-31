class WorkflowContext:

    def __init__(self):

        self.variables = {}

    def set(self, key, value):

        self.variables[key] = value

    def get(self, key, default=None):

        return self.variables.get(key, default)