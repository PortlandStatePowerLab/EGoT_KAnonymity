import enum, re, sys
import numpy as np
from numpy.lib.function_base import append
import pandas as pd
import string
from itertools import cycle
from tree_handler import Dist

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
def create_random_data(dist,size=50):
    # randomly add parents
    dist.add_level_rand('segment',10)
    dist.add_level_rand('xformer',5)
    dist.add_level_rand('DER',size)
    df = dist.export_to_df()
    return df
dist = Dist('substation')
print(dist)
print('-'*5,'CONSTRUCTING...','-'*5)
fname = 'random_ids.csv'
# if sys.argc > 3:

mode = sys.argv[1]
size = sys.argv[-1]
if mode != 'r':
    df = create_13_node_feeder(dist)
else:
    if size == mode:
        df = create_random_data(dist)
    else:
        df = create_random_data(dist,int(size))
print(dist)
print(df)
df.to_csv(fname,index = False)