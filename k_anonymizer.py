import sys
import numpy as np
import pandas as pd
# from transform import Transformer
import argparse
import matplotlib.pyplot as plt
sys.path.insert(-1,'Basic_Mondrian')
from mondrian import mondrian
from models.gentree import GenTree


class KAnonymizer:
    '''
        This class is a wrapper around Basic_Mondrian implementation
        See Basic_Mondrian: https://github.com/qiyuangong/Basic_Mondrian.git
    '''
    def __init__(self,fname:str):
        self.hs = [1,2,3,4,5,6,8,10,12,
            15,16,20,24,30,32,40,48,60,
            64,80,96,120,160,192, 240, 320
            ]
        '''
            Constructor
            fname: name of file containing data to be anonymized (csv)
                * The csv MUST have headers that reflect attribute values
        '''
        df = pd.read_csv(fname)
        self.df = self.extract_ders(df)
        self.data = self.df.values
        self.anonymized = None
        pass
    def anonymize(self,k:int =2,gen_scale:int = None,cols:list =None):
        '''
            Runs K-Anonymity on given data
            It assumes all data attributes are categorical
        '''
        cols = self.df.columns.values if cols==None else cols
        # pick H
        sz = len(self.df)
        if gen_scale is None:
            h = next((h for h in self.hs if h>=k),10)
            # h = k

        else:
            h = gen_scale

        self.h = h
        hierarchy = self.generate_hierarch(cols,h,len(self.data))
        # flip data
        flipped = np.flip(self.data,-1)
        
        anonymized,(ncp,t) = mondrian(hierarchy,flipped,k)
        anonymized = np.flip(anonymized,-1)
        self.anonymized = pd.DataFrame(anonymized,columns=cols)
        return self.anonymized,ncp,t
    def export_to_csv(self,output=None):
        '''
            Saves the anonymized version of data into a CSV
            output(str): name of output file
        '''
        assert output != None, 'Invalid output file name'
        assert not self.anonymized is None, 'No anonymized data found'
        print('exporting....')
        self.anonymized.to_csv(output,index=False)
        return
    def extract_ders(self,df):
        '''
            Splits and extracts DER column to produce seperate rows for each DER
            df (DataFrame): DataFrame containing DER IDs to process
        '''
        # conver everthing to be der related
        print('-'*10,'PREPROCESSING','-'*10)
        cols = df.columns
        # split
        df['DER'] = df['DER'].apply(lambda x: x.split('-'))
        # create new df w/ splitted values
        new_df = pd.DataFrame(df['DER'].tolist(),columns=cols)
        return new_df
    def generate_hierarch(self,names,gen_scale=5,data_size=1000):
        '''
            Generates hierarchy used by the Mondrian algorithm for EGoT IDs
            names (list): name of columns to generate hierarchies for
            gen_scale (int): number of DERs grouped together
            data_size (int): total number of DERs to use when generating the hierarchy --> should be same size of records in data
        '''
        hier = []
        d = {}
        # generate root for all names (might not be the best scheme)
        root = GenTree("*")
        d["*"] = root

        for name in reversed(names):
            print(f'generating generalization hierarchy for: {name}')
            # generate internal nodes (level 1)
            generic_intern = GenTree(f"{name}",root)
            d[f"{name}"] = generic_intern
            j = 0
            # using the range below is redundant ( it does more than we need it to )
            # because it assumes all names have the same size (# of xformers != # of DERs necessarily)
            for i in range(data_size):
                if i%gen_scale == 0:
                    j = i
                    n = f'{name} {j}-{j+gen_scale}'
                    # generate internal node (level 2)
                    generic = GenTree(n,generic_intern)
                    d[n] = generic
                # generate leaves
                n = f"{name}{i}"
                t = GenTree(n,generic,True)
                d[n] = t
            hier.append(d)
        return hier
    def preprocss(self,tranformer,df):
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
def get_count(df):
    '''
        Groups by all columns to produce count of unique rows in data
        df (DataFrame): DataFrame to process
    '''
    l = list(df.columns)
    return df.groupby(l).size().reset_index(name='count')
def join_ids(l):
    '''
        Reconstructs the IDs back to the original structure
        l (list): target data to reconstruct
    '''
    print('-'*10,'RECONSTRUCTING','-'*10)
    df = pd.DataFrame({})
    d = ['substation','feeder','xformer','DER']
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









def main():
    parser = argparse.ArgumentParser(description='Anonymize a CSV file.')
    parser.add_argument('-f', metavar='F', type=str, help='Input file name')
    parser.add_argument('-o', metavar='O', type=str, help='Output file name')
    parser.add_argument('-K', metavar='K', type=int, help='K used K-Anonymity',default=2)
    parser.add_argument('-H', metavar='H', type=int, help='H used Generalization Hierarchy',default=None)
    args = parser.parse_args()
    f = args.f
    o = args.o
    K = args.K
    H = args.H

    anonymizer = KAnonymizer(fname=f)
    d,n,t = anonymizer.anonymize(k=K,gen_scale=H)
    if o != None:
        anonymizer.export_to_csv(o)
    print('\nAfter anonymizing: \n',d)
    print(f'NCP:\t{round(n,3)}%')
    print(f'time:\t{round(t,3)}')
if __name__ == '__main__':
    main()
    exit()
