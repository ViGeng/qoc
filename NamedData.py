class NamedData:
    '''
    _FUNC, _DATA represent recursive boundrary conditions
    '''
    def __init__(self, name:str, func, data, result=None):

        self.name = name

        if func not in ['_FUNC', '_DATA']:
            assert type(func) == NamedData
            assert type(data) == NamedData

        self.func = func
        self.data = data
        self.result = result

    def check_params(self, para):
        print(para)
        if para in ['_FUNC', '_DATA']:
            return True
        if type(para) == NamedData:
            return True
        return False

    def reduce(self):
        if self.result is not None:
            return self.result
        if self.func in ['_FUNC', '_DATA']:
            self.result = self.data
            return self.data
        # reduce
        self.reduced_func = self.func.reduce()
        self.reduced_data = self.data.reduce()
        return self.reduced_func(self.reduced_data)
