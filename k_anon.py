import pandas as pd
from transform import Transformer

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



t = Transformer()
df = pd.read_csv(fname)
print(df)
df_ders = extract_ders(df)
print(df_ders)
print(preprocss(t,df_ders))

# df = pd.read_csv(f)
# df = get_count(df)

# print(df)
# print(preprocss(t,df))
# print(f"{'-'*10} BEFORE {k}-Anonymizing {'-'*10}")
# print(df[df['count']<k])
# print(f"{'-'*10} AFTER {k}-Anonymizing {'-'*10}")
# dfm = k_anon(df)
# print(dfm[dfm['count']<k])
