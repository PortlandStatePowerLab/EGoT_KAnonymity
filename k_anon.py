import pandas as pd

f = 'file.csv'
k = 2
def k_anon(df):
    #df['masked'] = pd.cut(df['BA'],bins=k)
    return df

def get_count(df):
    l = list(df.columns)
    return df.groupby(l).size().reset_index(name='count')

df = pd.read_csv(f)
df = get_count(df)


print(f"{'-'*10} BEFORE {k}-Anonymizing {'-'*10}")
print(df[df['count']<k])
print(f"{'-'*10} AFTER {k}-Anonymizing {'-'*10}")
dfm = k_anon(df)
print(dfm[dfm['count']<k])
