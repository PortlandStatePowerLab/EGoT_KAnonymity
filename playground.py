import pandas as pd
def isKAnonymized(df, k):
    for i, row in df.iterrows():
        query = ' & '.join([f'{col} == "{row[col]}"' for col in df.columns])
        rows = df.query(query)
        print(f"# of rows for query({query}) is {rows.shape[0]}")
        if rows.shape[0] < k:
            return False
    return True
def grouping(df):
    return df.groupby(['BA','substation']).size()
def distance(v,u):
    '''
        Distance between two records
        For our purposes, distance is defined as: 
            The number of columns the two records share
    '''
    cols = list(v.keys())
    d = 0
    shared = []
    for c in cols:
        if v[c] == u[c]:
            d+= 1
            shared.append(c)
    return d,tuple(shared)
def Anon(df):
    df['masked'] = pd.cut(df['BA'],bins=k)
    return df

k = 2
df = pd.read_csv('file.csv')
# print(isKAnonymized(df, k))
for i, row in df.iterrows():
    if i < len(df)-1:
        d,num = distance(row,df.loc[i+1])
    if d > 1:
        print(f"distance between {tuple(row)} && {tuple(df.loc[i+1])}\t= {d} at {num}")

print(grouping(df))
print(df.query('BA == "b3"'))