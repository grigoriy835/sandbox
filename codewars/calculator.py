# https://www.codewars.com/kata/5235c913397cbf2508000048/train/python


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Calculator(object):
    def evaluate(self, string: str):
        symbols = map(lambda x: float(x) if is_number(x) else x, string.split(' '))

        return self.count(list(symbols))

    def count(self, symbols: list):
        while 1: # remove "()"
            i = -1
            for si in range(0, len(symbols)):
                if symbols[si] == '(':
                    i = si
                if symbols[si] == ')':
                    symbols = symbols[0:i] + [self.count(symbols[i+1:si])] + symbols[si+1:]
                    break
            if i == -1:
                break

        while 1: # remove number negation
            flag = True
            for si in range(0, len(symbols)):
                if symbols[si] == '-' and (si == 0 or isinstance(symbols[si-1], str)):
                    symbols = symbols[0:si] + [-symbols[si+1]] + symbols[si + 2:]
                    flag = False
                    break
            if flag:
                break

        while 1:
            flag = True
            for si in range(0, len(symbols)):
                if symbols[si] == '*':
                    symbols = symbols[0:si-1] + [symbols[si-1] * symbols[si+1]] + symbols[si + 2:]
                    flag = False
                    break
                if symbols[si] == '/':
                    symbols = symbols[0:si-1] + [symbols[si-1] / symbols[si+1]] + symbols[si + 2:]
                    flag = False
                    break

            if flag:
                break

        while 1:
            flag = True
            for si in range(0, len(symbols)):
                if symbols[si] == '-':
                    symbols = symbols[0:si - 1] + [symbols[si - 1] - symbols[si + 1]] + symbols[si + 2:]
                    flag = False
                    break
                if symbols[si] == '+':
                    symbols = symbols[0:si - 1] + [symbols[si - 1] + symbols[si + 1]] + symbols[si + 2:]
                    flag = False
                    break

            if flag:
                break

        return symbols[0]


calc = Calculator()

print(calc.evaluate('- 5 * 60 + ( - 3 * - 80 / 1 ) + 50 / 5 * - ( - 3 - 1 )'))



#//////////////////////-------------------------------------------------best

import operator
OP_D = {'/': operator.truediv,
        '*': operator.mul,
        '+': operator.add,
        '-': operator.sub}
OP_LST = [{'/', '*'}, {'-', '+'}]

class Calculator(object):
    def evaluate(self, s):
        lst = s.split()
        print(lst)
        for preceed in range(2):
            i = 0
            while i < len(lst):
                if lst[i] in OP_LST[preceed]:
                    lst[i-1] = OP_D[ lst[i] ](float(lst.pop(i-1)), float(lst.pop(i)) )
                else:
                    i+=1
        return round(float(lst[0]), 10)