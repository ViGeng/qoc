from NamedData import NamedData


def test_reduce():
    func = lambda x: x + 1
    nd = NamedData(func, 1)
    assert nd.reduce() == 2


if __name__ == '__main__':
    test_reduce()
    print('Test passed')
