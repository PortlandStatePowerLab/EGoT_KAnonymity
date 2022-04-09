import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import k_anonymizer #import KAnonymizer
import argparse

parser = argparse.ArgumentParser(description='Anonymize a CSV file.')
parser.add_argument('-f', metavar='F', type=str, help='Input file name')

args = parser.parse_args()
f = args.f
norm_ks,norm_ns, norm_hs = [],[],[]
size = len(pd.read_csv(f))//2

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

name = 'ncp_vs_k_1000_'
h_vals = [2,4,5,6,8,10,12,14,15]
anonymizer = k_anonymizer.KAnonymizer(fname=f)
run_normal = True
for h in h_vals[1:3]:
    ks = []
    ns = []
    hs = []
    for i in range(1,size+2):
        ks.append(i)
        d,n,t = anonymizer.anonymize(k=i,gen_scale=i)
        hs.append(anonymizer.h)
        ns.append(n)

        if run_normal:
            d,n,t = anonymizer.anonymize(k=i)
            norm_ks.append(i)
            norm_hs.append(anonymizer.h)
            norm_ns.append(n)
    plt.plot(ks,ns)
    plt.plot(ks,norm_ns)
    plt.grid() 

    plt.legend([f'h = k',f'h = {h}'])
    plt.title('NCP vs K')
    plt.ylabel('NCP (%)')
    plt.xlabel('K')
    plt.xticks(list(range(0,len(ks)+1,size//10)))
    
    plt.savefig(name+f'{h}.png')
    plt.close()
    run_normal = False

con = list(zip(ks,hs,ns))
# print(list(filter(lambda x: x[-1] <10,con)))
# print('\n')
# print(list(filter(lambda x: x[-1] >4,con)))
