#  https://www.codewars.com/kata/54eb33e5bc1a25440d000891/train/python
from math import sqrt


def decompose(n):
    def serve(summ: int, numbers: list):
        for index in range(0, len(numbers)):
            new_summ = summ - numbers[index]
            if new_summ == 0:
                return [numbers[index]]
            if new_summ > 0:
                result = serve(new_summ, numbers[index+1:])
                if result:
                    return [numbers[index]] + result

    numbers = list(map(lambda x: x*x, list(range(1, n))))
    numbers.reverse()
    result = serve(n*n, numbers)
    if result:
        result = list(map(sqrt, result))
        result.reverse()
    return result



print(decompose(5))
print(decompose(10))
print(decompose(15))
print(decompose(20))
print(decompose(25))
print(decompose(26))
print(decompose(27))
print(decompose(28))


##/////////////////------------------------------------------best

def decompose2(n):
    def _recurse(s, i):
        if s < 0:
            return None
        if s == 0:
            return []
        for j in xrange(i-1, 0, -1):
            sub = _recurse(s - j**2, j)
            if sub != None:
                return sub + [j]
    return _recurse(n**2, n)