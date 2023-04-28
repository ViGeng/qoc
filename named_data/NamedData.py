import named_data

class NamedData:
    '''
    _FUNC, _DATA represent recursive boundrary conditions
    '''
    def __init__(self, name:str, func, *data):

        self.result = None
        self.name = name

        if func not in named_data.COMPs:
            assert type(func) == NamedData
            data = list(data)
            for d in data:
                assert type(d) == NamedData

        self.func = func
        self.data = data

    def reduce(self):
        if self.result is not None:
            return self.result
        if self.func in named_data.COMPs:
            self.result = self.data
            return self.data
        # reduce
        reduced_func = self.func.reduce()
        reduced_data = self.flatten_list([d.reduce() for d in self.data])
        return reduced_func[0](reduced_data)

    def flatten_list(self, lst):
        flattened = []
        for item in lst:
            if isinstance(item, list) or isinstance(item, tuple):
                flattened.extend(self.flatten_list(item))
            else:
                flattened.append(item)
        return flattened

    def __str__(self):
        return f'''
        NamedData(
        name={self.name},
        data={self.data},
        )
        '''
