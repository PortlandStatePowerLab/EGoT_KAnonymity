import enum, re, sys
import numpy as np
from numpy.lib.function_base import append
import pandas as pd
import string
from itertools import cycle
from tree_handler import Dist
'''
max_segs = {
    633: 106,
    611: 39,
}

# file name
o_fname = 'file.csv'

# Balancing areas, substations, feeders, and transformers
cols = ['seg','xformer','sp']
# samples to generate
MAX_SEG = max_segs[611]
# DER density on segment
density = 1 # 10%
# MAX cap for xformers
MAX_X = int(density * MAX_SEG)

segs_num = 1

# alphabet:
letters = list(string.ascii_lowercase[:3])


sps = []
s = 0


def collapse(record):
    label,xs = record
    return list(map(lambda x: f'{label}{x}',xs))

while s < MAX_X:
    # randomly pick your xformer capacity
    num_of_houses = np.random.randint(1,abs(s-MAX_X)+1)
    # create houses of xformer sz
    houses = list(range(1,num_of_houses+1))
    s += len(houses)
    sps.append(houses)

df = pd.DataFrame({})
for seg,(xform,sp) in zip(cycle(range(1,segs_num+1)),enumerate(sps,1)):
    # for t,sp in :
    sz = len(sp)
    raw = list(zip(letters,[[seg],[xform],sp]))
    rec = []
    for r in raw:
        c = collapse(r)
        if len(c)<sz:
            c = c * sz 
        rec.append(c)
    record = list(zip(*rec))
    df = df.append(record,ignore_index=True)

df.columns = cols
print(df)
'''

# In 13 node feeder: 
#   - segs are nodes
#   - we have 13 nodes 
#       - we are only using 11 nodes (1 is 480v node - not used in res areas {634} & the other is a branch of the main nodes {6321})
#   - each seg has 5 xformers
#   - each transformer has 40 sp


def create_13_node_feeder(dist):
    _,feeders = dist.add_level('feeder',5) # feeder should before the segment
    _,seg1 = dist.add_level('segment',1,lvls=feeders[1:2])
    _,seg2 = dist.add_level('segment',3,lvls=feeders[2:]) # feeder should before the segment
    seg1.extend(seg2[:1])
    seg2 = seg2[1:]
    # segs.extend(seg)
    _,xformer = dist.add_level('xformer',5,lvls=seg1)
    _,xformers = dist.add_level('xformer',10,lvls=seg2[:2])
    xformers.extend(xformer)
    # add 15 xformers to the remaining segs
    _,xformer = dist.add_level('xformer',15,lvls=seg2[2:])
    xformers.extend(xformer)
    _,ders = dist.add_level('DER',8,leave=True,lvls=xformers)
    # dist.add_level('xformer',5)
    # dist.add_level('DER',8,leave=True)

    # ------------------- adding 10 more segs to the middle segs ---------------
    # _,lvl=dist.add_level('xformer',10,lvls=seg_names[2:-2],id_range=list(range(5,15)))
    # dist.add_level('DER',8,leave=True,lvls=lvl)

    # ------------------ adding 5 more segs to the last segs -------------------
    # _,lvl=dist.add_level('xformer',5,lvls=seg_names[-2:],id_range=list(range(5,10)))
    # dist.add_level('DER',8,leave=True,lvls=lvl)
    df = dist.export_to_df()
    return df
def create_random_data(dist):
    # randomly add parents
    dist.add_level_rand('segment',10)
    dist.add_level_rand('xformer',5)
    dist.add_level_rand('DER',50)
    df = dist.export_to_df()
    return df
dist = Dist('substation')
print(dist)
print('-'*5,'CONSTRUCTING...','-'*5)
fname = 'random_ids.csv'
mode = sys.argv[-1]
if mode != 'r':
    df = create_13_node_feeder(dist)
else:
    df = create_random_data(dist)
print(dist)
print(df)
df.to_csv(fname,index = False)