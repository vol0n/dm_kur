import string
import config as c
import operations as op


def next():
    if c.i+1 < len(c.line):
        return c.line[c.i+1]
    return '\0'


def move(shift=1):
    if c.i+shift < len(c.line):
        c.i += shift


def lexan():
    while next() == ' ':
        move()
    if next() in string.digits:
        c.lexeme = ''
        while next() in string.digits:
            c.lexeme += next()
            move()
        c.tokenval = c.lexeme
        return 'num'
    elif next() in string.ascii_letters:
        c.lexeme = ''
        while next() in string.ascii_letters or next() in string.digits:
            c.lexeme += next()
            move()
        c.tokenval = c.lexeme
        while next() == ' ':
            move()
        if next() == '=':
            move()
            return 'id='
        return 'id'
    elif next() in c.symbols:
        c.tokenval = next()
        move()
        return c.tokenval
    elif next() == '\0':
        c.tokenval = 'eof'
        return 'eof'
    else:
        print("Lexycal analyser fail: unknown symbol: ", next())
        move()
        return 'unknown'


def match(token):
    if token == c.lookahead:
        c.lookahead = lexan()
    else:
        print("Error in match lookahead: ", c.lookahead, " token: ", token)


def parse():
    c.lookahead = lexan()
    e = None
    if c.lookahead == 'id=':
        name = c.tokenval
        match('id=')
        if name in c.symtable and c.symtable[name] == 'keyword':
            print("Can't use keyword as an id")
        else:
            try:
                e = expr()
            except ArithmeticError:
                print(c.ErrorText)
            if e is not None:
                c.symtable[name] = e
                print(name, " = ", c.symtable[name])
                if c.OverflowFlag:
                    print("Warning: overflow has happened during calculation!")
                    c.OverflowFlag = False
    else:
        try:
            e = expr()
        except ArithmeticError:
            print(c.ErrorText)
        if e is not None:
            print(e)
            if c.OverflowFlag:
                print("Warning: overflow has happened during calculation!")
                c.OverflowFlag = False



def expr():
    res = term()
    if res is not None:
        while True:
            if c.lookahead == '+':
                match(c.lookahead)
                operand2 = term()
                if operand2 is not None:
                    res = res + operand2
                    continue
            elif c.lookahead == '-':
                match('-')
                op2 = term()
                if op2 is not None:
                    res = res - op2
                    continue
            elif (
                c.lookahead not in c.symbols and
                c.lookahead != 'unknown' and c.lookahead != 'eof'
            ):
                print("SyntaxError")
                return res
            else:
                return res


def term():
    res = factor()
    if res is not None:
        while True:
            if c.lookahead == '*':
                match('*')
                op2 = factor()
                if op2 is not None:
                    res = res * op2
                    continue
                return None
            elif c.lookahead == '/':
                match('/')
                op2 = factor()
                if op2 is not None:
                    res = res / op2
                    continue
            elif (
                c.lookahead not in c.symbols and
                c.lookahead != 'unknown' and c.lookahead != 'eof'
            ):
                print("SyntaxError")
                return res
            else:
                return res


def factor():
    if c.lookahead == '(':
        match('(')
        res = expr()
        if res is not None:
            match(')')
            return res
        return None
    elif c.lookahead == 'num':
        res = op.Num(c.tokenval)
        match('num')
        return res
    elif c.lookahead == 'id':
        name = c.tokenval
        match('id')
        if name in c.symtable:
            return c.symtable[name]
        if name != 'q':
            print("Value of ", c.tokenval, " unknown!")
        return None
    elif c.lookahead == '-':
        match('-')
        if c.lookahead == 'num':
            res = op.Num(c.tokenval)
            res = op.Num() - res
            match('num')
            return res
        elif c.lookahead == 'id':
            name = c.tokenval
            match('id')
            if name in c.symtable:
                if c.symtable[name] == 'keyword':
                    print("Can't use keyword as id!")
                else:
                    res = op.Num()-c.symtable[name]
                    return res
            else:
                print("Undefined name ", name)
        print('syntax error: ', c.line[c.i-1::])
        return None
    else:
        if c.lookahead != 'unknown':
            print('syntax error', c.lookahead)
        return None


