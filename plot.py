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
norm_ks,norm_ns = [],[]
size = (len(pd.read_csv(f))+1)//2 
print(size)

CB91_Blue = '#2CBDFE'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'

color_list = [CB91_Blue, CB91_Purple, CB91_Violet]

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

name = 'ncp_vs_k_500_normal.png'

anonymizer = k_anonymizer.KAnonymizer(fname=f)

ks = []
ns = []
for i in range(1,size+2):
    ks.append(i)
    d,n,t = anonymizer.anonymize(k=i,gen_scale=i)
    # hs.append(anonymizer.h)
    norm_ns.append(n)
    print('1 (norm): --->\n',d)
    d,n,t = anonymizer.anonymize(k=i)
    norm_ks.append(i)
    print('2: ===>\n',d)
    ns.append(n)

plt.plot(ks,norm_ns)
plt.grid() 

plt.legend(['H = K'])
plt.title('NCP vs K')
plt.ylabel('NCP (%)')
plt.xlabel('K')
plt.xticks(list(range(0,len(ks)+1,size//10)))

plt.savefig(name)
plt.close()
