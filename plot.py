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
for i in range(1,52):
    ks.append(i)
    anonymizer = k_anonymizer.KAnonymizer(fname=f)
    d,n = anonymizer.anonymize(k=i,gen_scale=i)
    ns.append(n)
    print('\nAfter anonymizing: \n',d)
    print(n)
plt.plot(ks,ns)
plt.title('K vs NCP')
plt.ylabel('NCP (%)')
plt.xlabel('K')
plt.xticks(list(range(0,len(ks)+1,2)))
plt.savefig('ks_vs_ns.png',fmt='PNG')
print('KS: ',ks,'\n')
print('NS: ',ns)