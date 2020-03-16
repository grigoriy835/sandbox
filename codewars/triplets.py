# https://www.codewars.com/kata/53f40dff5f9d31b813000774/train/python
from functools import reduce
import time


def recoverSecret(triplets):
    result = []

    while 1:
        right = True
        for tr in triplets:
            i = 0
            if tr[0] in result:
                i = result.index(tr[0])
            else:
                result.insert(0, tr[0])
                i = 0
                right = False

            if tr[1] in result:
                i1 = result.index(tr[1])
                if i1 < i:
                    result.pop(i1)
                    result.insert(i, tr[1])
                    right = False
                else:
                    i = i1
            else:
                i += 1
                result.insert(i, tr[1])
                right = False

            if tr[2] in result:
                i2 = result.index(tr[2])
                if i2 < i:
                    result.pop(i2)
                    result.insert(i, tr[2])
                    right = False
                else:
                    i = i2
            else:
                i += 1
                result.insert(i, tr[2])
                right = False

        if right:
            return ''.join(result)



triplets = [
    ['t', 'u', 'p'],
    ['w', 'h', 'i'],
    ['t', 's', 'u'],
    ['a', 't', 's'],
    ['h', 'a', 'p'],
    ['t', 'i', 's'],
    ['w', 'h', 's']
]

secret = "whatisup"
print(recoverSecret(triplets))

#///////////----------------------best

def recoverSecret(triplets):
    r = list(set([i for l in triplets for i in l]))
    for l in triplets:
        fix(r, l[1], l[2])
        fix(r, l[0], l[1])
    return ''.join(r)


def fix(l, a, b):
    """let l.index(a) < l.index(b)"""
    if l.index(a) > l.index(b):
        l.remove(a)
        l.insert(l.index(b), a)

