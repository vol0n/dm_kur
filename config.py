import numpy as np


add_table = add_overflow_table = mul_table = mul_overflow_table = None
line = tokenval = i = symbols = symtable = lookahead = None
ErrorText = None
OverflowFlag = False


def init():
    global line, tokenval, i, symbols, symtable
    line = None
    tokenval = None
    i = -1
    symbols = '+-/*=()'
    symtable = {'nod': 'keyword', 'nok': 'keyword'}


def calc2(k, j, order):
    x = order.index(k)
    y = order.index(j)
    res = x+y
    res2 = x*y
    n = len(order)
    return order[res % n], res // n, order[res2 % n], res2 // n


def init_tables(order):
    global add_table, add_overflow_table, mul_table, mul_overflow_table
    n = len(order)
    add_table = np.zeros((n, n), dtype=int)
    add_overflow_table = np.zeros((n, n), dtype=int)
    mul_table = np.zeros((n, n), dtype=int)
    mul_overflow_table = np.zeros((n, n), dtype=int)
    for k in range(n):
        for j in range(n):
            ret = calc2(k, j, order)
            add_table[k, j] = ret[0]
            add_overflow_table[k, j] = ret[1]
            mul_table[k, j] = ret[2]
            mul_overflow_table[k, j] = ret[3]


