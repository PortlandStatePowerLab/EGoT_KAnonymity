import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.metrics import silhouette_samples


df = pd.read_csv('file.csv')
print(df)
kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0).fit(df)
