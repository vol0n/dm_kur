import config as c
import numpy as np
import pandas as pd



def print_table(t):
    df = pd.DataFrame(t)
    print(df)
    print()


class Arithmetic:
    def __init__(self, alphabet, plus_one, r=8, zero=0, one=1):
        self.alphabet = alphabet
        self.plus_one = [alphabet.index(x) for x in plus_one]
        self.r = r
        self.n = len(alphabet)
        self.zero = zero
        self.one = one
        self.add, self.addOV, self.mul, self.mulOV = [np.zeros((self.n, self.n), dtype=int) for i in range(4)]
        self.order = [zero, one]
        for i in range(2, self.n):
            self.order.append(self.plus_one[self.order[i-1]])
        for i in range(self.n):
            for j in range(self.n):
                self.add[i, j], self.addOV[i, j] = self.sum_ov(i, j)
                self.mul[i, j], self.mulOV[i, j] = self.mul_ov(i, j)
        print("Order: ", self.order)
        print("Add table: \n")
        print_table(self.add)
        print("Add overflow table: \n")
        print_table(self.addOV)
        print("Mul talbe: \n")
        print_table(self.mul)
        print("Mul overflow table: \n")
        print_table(self.mulOV)

    def sum_ov(self, i, j):
        ov = self.zero
        r = self.zero
        while r != j:
            i = self.plus_one[i]
            r = self.plus_one[r]
            if i == self.zero:
                ov = self.plus_one[self.zero]
        return i, ov

    def mul_ov(self, i, j):
        ov = self.zero
        m = self.zero
        s = self.zero
        while m != j:
            s, current_ov = self.sum_ov(s, i)
            ov = self.sum_ov(ov, current_ov)[0]
            m = self.plus_one[m]
        return s, ov

#16723450
class Num:
    a = Arithmetic(alphabet='01234567', plus_one='16723450')
    r = a.r
    n = a.n
    zero = a.zero
    one = a.one
    order = a.order
    alphabet = a.alphabet
    plus_one = a.plus_one
    add, addOV, mul, mulOV = a.add, a.addOV, a.mul, a.mulOV
    min = alphabet[order[-3]] + alphabet[order[0]]*(r-1)
    max = alphabet[order[-4]] + alphabet[order[-1]]*(r-1)

    def __init__(self, arg=a.alphabet[a.zero]*a.r):
        self.remainder = None
        if len(arg) > Num.r:
            c.ErrorText = "Too many symbols in a word: {} !".format(arg) + " Max is {}".format(Num.r)
            raise ArithmeticError
        if isinstance(arg, list):
            arg = ''.join([str(x) for x in arg])
        for j in arg:
            if j not in Num.alphabet:
                c.ErrorText = "Wrong symbol in a word: {} : ".format(arg) + "{}. Set of correct symbols for word: {}".format(j, Num.alphabet)
                raise ArithmeticError
        self.word = [Num.zero]*(Num.a.r - len(arg)) + [Num.a.alphabet.index(x) for x in arg]

    def __getitem__(self, item):
        assert item < Num.a.r
        return self.word[item]

    def __setitem__(self, key, value):
        assert key < Num.a.r
        self.word[key] = value

    def __add__(self, other):
        carry_over = Num.a.zero
        overflow = Num.a.zero
        isNeg1, isNeg2 = [1 if x[0] in Num.a.order[-3:] else 0 for x in (self, other)]
        res = Num()
        for i in reversed(range(Num.a.r)):
            sum = Num.add[self[i], other[i]]
            overflow = Num.addOV[self[i], other[i]]
            res[i] = Num.add[sum, carry_over]
            carry_over = overflow if overflow else Num.addOV[sum, carry_over]
        isNeg = 1 if res[0] in Num.order[-3:] else 0
        if carry_over or (isNeg1 == isNeg2 and isNeg1 != isNeg):
            c.OverflowFlag = True
        return res

    def __mul__(self, other):
        res = Num()
        k = 0
        for i in reversed(range(Num.r)):
            tmp = Num()
            ov_mul = ov_sum = Num.zero
            for j in reversed(range(Num.r)):
                if j-k < 0:
                    break
                product = Num.mul[self[j], other[i]]
                tmp[j-k] = Num.add[product, ov_mul]
                ov1 = Num.addOV[product, ov_mul]
                ov2 = Num.addOV[tmp[j-k], ov_sum]
                tmp[j-k] = Num.add[tmp[j-k], ov_sum]
                ov_mul = Num.mulOV[self[j], other[i]]
                ov_sum = Num.add[ov1, ov2]
            # if not (Num(str(ov_sum))+Num(str(ov_mul))).isnull():
            #     c.OverflowFlag = True
            k += 1
            res = res + tmp
        return res

    def __sub__(self, other):
        complement = Num()
        for j in range(Num.a.r):
            complement[j] = np.where(Num.add[other[j]] == Num.a.order[-1])[0][0]
        complement = complement + Num([Num.zero]*(Num.r-1) + [Num.one])
        return self + complement

    def compare(self, other, isStrict=False):
        k = 0
        while k < Num.r and self[k] == other[k]:
            k += 1
        if k == Num.r:
            return not isStrict
        isNeg1, isNeg2 = [1 if x[0] in Num.a.order[-3:] else 0 for x in (self, other)]
        if not isNeg1 and not isNeg2:
            if Num.a.order.index(self[k]) < Num.a.order.index(other[k]):
                return False
            return True
        if isNeg1 and not isNeg2:
            return False
        if isNeg2 and not isNeg1:
            return True
        return other.abc().compare(self.abc, isStrict)

    def isnull(self):
        for d in self.word:
            if d != self.zero:
                return False
        return True

    def abc(self):
        if self[0] in (Num.order[-3:]):
            return Num()-self
        return self

    def __truediv__(self, other):
        res = Num()
        if other.isnull() and self.isnull():
            c.ErrorText = "[-" + (Num()-Num(Num.min)).__repr__() + ", " + (Num(Num.max)).__repr__() + "]"
            raise ArithmeticError
        if other.isnull():
            c.ErrorText = "Division by zero: undefined value!"
            raise ArithmeticError
        isPos1 = self.compare(Num(), True)
        isPos2 = other.compare(Num(), True)
        a = self.abc()
        b = other.abc()
        while a.compare(b):
            a = a - b
            res = res + Num(Num.a.alphabet[Num.one])

        res.remainder = a
        if not isPos1:
            if a.isnull():
                res = Num()-res
                res.remainder = a
                return res
            res = Num() - (res+Num(Num.alphabet[Num.one]))
            res.remainder = b-a
            return res
        if isPos1 and not isPos2:
            res = Num() - res
            res.remainder = a
            return res
        return res

    def __repr__(self):
        res = ''
        #if self.isoverflow:
         #   res += "Warning: overflow happened!\n"
        if self.isnull():
            return res + Num.a.alphabet[Num.zero]
        tmp = self
        if self[0] in Num.order[-3:]:
            res += '-'
            tmp = Num(list(map(lambda x: Num.a.order[Num.n-1-Num.a.order.index(x)], self.word)))+Num(Num.alphabet[Num.one])
        res += (''.join(map(lambda x: Num.a.alphabet[x], tmp.word))).lstrip(Num.alphabet[Num.zero])
        if self.remainder is not None:
            res = "div = " + res + " mod = " + self.remainder.__repr__()
        return res
