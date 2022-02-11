import sys
import numpy as np
import pandas as pd
from transform import Transformer
sys.path.insert(-1,'Basic_Mondrian')
from mondrian import mondrian
from models.gentree import GenTree

fname = 'random_ids.csv'
k = 2
def k_anon(df):
    # df['masked'] = pd.cut(df['BA'],bins=k)
    print(df.groupby(['BA','substation']).size())
    return df

def get_count(df):
    l = list(df.columns)
    return df.groupby(l).size().reset_index(name='count')

def preprocss(tranformer,df):
    '''
        changes categorical columns into numerical.
        Each categorical column results in 2 numerical ones (one for the transform string part and another for the int part)
        ASSUMPTION: the pattern each categorical cell is: wd
            * where w is a one or more chars
            * where d is one or more digits
            * this means the string part is ALWAYS before the digit part (see the regex used)
    '''
    cols = df.columns
    a = '_num'
    for c in cols:
        print('processing column: ',c)
        try:
            # split column into string and numerical part
            d = df[c].str.extract(r'([a-zA-Z]+)(\d)')
            df[c] = d[0] # replace col with only string part
            # apply transformation onto columns
            # 1. grab unique values
            v = df[c].unique()
            # 2. add to tranformer (ensure the transformer has any new keys)
            tranformer.add(v)
            # 3 transform
            df[c] = tranformer.transform(df[c])
            df[c+a] = d[1] # create col_num
        except Exception as e:
            # extraction failed (pattern was incorrect - either completely numeric values or completely str value)
            print(e)
            # ignore column & continue
            continue
    return df

def extract_ders(df):
    # conver everthing to be der related
    print('-'*10,'PREPROCESSING','-'*10)
    cols = df.columns
    # split
    df['der'] = df['der'].apply(lambda x: x.split('-'))
    # create new df w/ splitted values
    new_df = pd.DataFrame(df['der'].tolist(),columns=cols)
    return new_df

def join_ids(l,cols):
    print('-'*10,'RECONSTRUCTING','-'*10)
    df = pd.DataFrame({})#,columns = cols)
    d = ['substation','feeder','xformer','ders']
    for r in l:
        t = {}
        t[d[0]] = r[0]
        last = r[0]
        for i in range(1,len(r)-1):
            #print(i)
            t[d[i]] = '-'.join([last,r[i]])
            last = r[i]
        df = df.append(list(t),ignore_index=True)
    return df

def Gen_hier(names,gen_scale=5,data_size=1000):
    hier = []
    d = {}
    # generate root for all names (might not be the best scheme)
    root = GenTree("*")
    d["*"] = root

    for name in names:
        print(f'generalizing: {name}')
        # generate internal nodes (level 1)
        generic_intern = GenTree(f"{name}",root)
        d[f"{name}"] = generic_intern
        j = 0
        # using the range below is redundant ( it does more than we need it to )
        # because it assumes all names have the same size (# of xformers != # of DERs necessarily)
        for i in range(data_size):
            if i%gen_scale == 0:
                j = i
                # generate internal node (level 2)
                generic = GenTree(f"{name} {j}-{j+gen_scale}",generic_intern)
                d[f"{name} {j}-{j+gen_scale}"] = generic
            # generate leaves
            n = f"{name}{i}"
            t = GenTree(n,generic,True)
            d[n] = t
        hier.append(d)
    return hier

t = Transformer()
df = pd.read_csv(fname)
#print(df)
df_ders = extract_ders(df)
ders = df_ders.values
for k in range(5):
    print(f"{'-'*10} ORIGINAL k = {k} {'-'*10}")
    ders = list(map(lambda x: list(reversed(x)),ders))[:4]
    for d in ders:
        print(d)
    # ders = list(map(lambda x: list(reversed(x)),ders))
    h = k
    while h%5 != 0 or h ==0:
        h += 1
    print('-'*50,'>',h)

    h = Gen_hier(['DER','xformer','segment','feeder','substation'],gen_scale=h)
    print(f"{'-'*10} Anonymizing k = {k} {'-'*10}")
    r,v = mondrian(h,ders,k)

    r = list(map(lambda x: list(reversed(x)),r))
    #print(join_ids(r,cols=df_ders.columns))
    d = pd.DataFrame(r)
    print(d.values)
    print(v[0])
