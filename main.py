import random
from NamedData import NamedData

FUNC = '_FUNC'
DATA = '_DATA'


def get_nd_func(type: str) -> NamedData:
    if type == 'func/list_sum':
        def add_list(num_list: list) -> int:
            sum = 0
            for num in num_list:
                sum += num
            return sum

        return NamedData(
            'func/list_sum',
            FUNC,
            add_list,
        )


def get_nd_data(type_str: str):
    if type_str == 'data/123':
        list = [1, 2, 3]
        return NamedData(
            'data/123',
            DATA,
            list,
        ), sum(list)
    if type_str == 'data/2random':
        # Generate two random numbers
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)
        # Create a list with the two numbers
        numbers = [num1, num2]
        return NamedData(
            'data/2random',
            DATA,
            numbers,
        ), sum(numbers)

def get_opaque_nd_case():
    data, expected = get_nd_data('data/2random')
    add2random = NamedData(
        'data/add2random',
        get_nd_func('func/list_sum'),
        data
    )
    return add2random, expected


def get_transparent_nd_case():

    data, expected = get_nd_data('data/123')
    add123 = NamedData(
        'data/add123',
        get_nd_func('func/list_sum'),
        data
    )
    return add123, expected


def test_func():
    nd_list_sum, expected_value = get_transparent_nd_case()
    assert nd_list_sum.reduce() == expected_value
    print('Test test_transparent_func passed!')

    add2random, expected_value = get_opaque_nd_case()
    assert add2random.reduce() == expected_value
    print('Test test_opaque_func passed!')

def main():
    test_func()

if __name__ == '__main__':
    main()
