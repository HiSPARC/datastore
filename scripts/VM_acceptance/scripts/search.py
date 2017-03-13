"""
show contents of datastore pickles
"""

from __future__ import print_function

import os
import pickle
from collections import defaultdict

entries = os.listdir('.')

totals = defaultdict(int)
for fn in entries:
    if fn[0:3] != 'tmp':
        continue
    print(fn)
    with open(fn, 'rb') as f:
        try:
            data = pickle.load(f)
        except:
            continue
    event_list = data['event_list']
    d = defaultdict(int)
    for event in event_list:
        upl_code = event['header']['eventtype_uploadcode']
        d[upl_code] += 1
        totals[upl_code] += 1
    print (fn, d)
print(totals)
