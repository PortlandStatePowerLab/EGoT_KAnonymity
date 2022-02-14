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
ks = []
ns = []
size = len(pd.read_csv(f))
for i in range(1,size+2):
    ks.append(i)
    anonymizer = k_anonymizer.KAnonymizer(fname=f)
    d,n,t = anonymizer.anonymize(k=i)
    ns.append(n)
plt.plot(ks,ns)
plt.title('K vs NCP')
plt.ylabel('NCP (%)')
plt.xlabel('K')
plt.xticks(list(range(0,len(ks)+1,size//10)))
plt.savefig('ks_vs_ns.png',fmt='PNG')
print('KS: ',ks,'\n')
print('NS: ',ns)