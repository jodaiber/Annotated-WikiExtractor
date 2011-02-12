# -*- coding: utf-8 -*-

import sys
import pickle

page = []
for line in sys.stdin:
    line = line.decode('utf-8').strip()
    if line == '<page>':
        page = []
    elif line == '</page>':
        print pickle.dumps(page)
    else:
        page.append(line)