import parser as ps
import config as c
import numpy as np
import operations as op

c.init()
while c.line != 'q':
    c.line = input('>> ')
    ps.parse()
    c.i = -1
    c.tokenval = None
