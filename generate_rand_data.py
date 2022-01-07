import numpy as np
import pandas as pd
import string

def random_char(x)->str:
    return f'{a[np.random.choice(len(a))]}{x}'

# Balancing areas, substations, feeders, and transformers
cols = ['BA','substation','feeder','transformer']
# samples to generate
n = 1000
# uniques
l = 1
h = 5

# size of alphabet
s = 5
# alphabet:
a = string.ascii_lowercase[:s]

# file name
f = 'file.csv'

# generate 100 rows w/ 4 columns (for BA-sub-feed-trans)
d = np.random.randint(l,h, size=(n,len(cols)))

df = pd.DataFrame(d,columns = cols)

for c in cols:
    df[c] = df[c].apply(random_char)

print(df)


df.to_csv(f,index=False)
