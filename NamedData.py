class NamedData:
    def __init__(self, func, data):
        self.func = func
        self.data = data
        self.result = None

    def my_function(self):
        # function code here
        pass

    def reduce(self):
        if self.result is None:
            self.result = self.func(self.data)
        return self.result
