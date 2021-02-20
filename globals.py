def init():
    global line, tokenval, i, symbols, symtable
    line = input("Enter data: ")
    tokenval = None
    i = -1
    symbols = '+-/*='
    symtable = {'nod': 'keyword', 'nok': 'keyword'}

