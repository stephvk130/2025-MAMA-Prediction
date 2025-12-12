#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephaniechen
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


## Import Data
song_data = pd.read_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Song_Data.csv")


## Ranking Model

# Normalize Columns
normalize_col = ['popularity_score', 'mv_view_count', 'mv_like_count', 'mv_comment_count']

scaler = MinMaxScaler()
song_data_norm = song_data.copy()
song_data_norm[normalize_col] = scaler.fit_transform(song_data_norm[normalize_col])

# weighted rank
song_w = {"popularity_score": 0.45, "mv_view_count": 0.10, "mv_like_count": 0.25, "mv_comment_count": 0.20}

song_data_norm["weighted_score"] = (song_data_norm["popularity_score"] * song_w["popularity_score"] +
                                    song_data_norm["mv_view_count"] * song_w["mv_view_count"] +
                                    song_data_norm["mv_like_count"] * song_w["mv_like_count"] +
                                    song_data_norm["mv_comment_count"] * song_w["mv_comment_count"])

song_ranked = song_data_norm.sort_values("weighted_score", ascending = False)
song_ranked["rank"] = song_ranked["weighted_score"].rank(method = "first", ascending = False).astype(int)
song_ranked.insert(0, "rank", song_ranked.pop(song_ranked.columns[-1]))

song_ranked.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Song_Weighted_Rank.csv", index = False)


## PCA

song_pca = song_data_norm[normalize_col]

pca = PCA(n_components = 1)
pca_components = pca.fit_transform(song_pca)

song_data_pca = song_data_norm.drop(['weighted_score'], axis = 1)
song_data_pca["PC1"] = pca_components[:,0]

song_data_pca = song_data_pca.sort_values("PC1", ascending = False)
song_data_pca["rank"] = song_data_pca["PC1"].rank(method = "first", ascending = False).astype(int)
song_data_pca.insert(0, "rank", song_data_pca.pop(song_data_pca.columns[-1]))

song_data_pca.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Song_PCA_Rank.csv", index = False)


## K-Means Clustering

# Elbow Plot

inertias = []
for k in range(1,10):
    kmeans = KMeans(n_clusters = k, random_state = 41).fit(song_data_norm[normalize_col])
    inertias.append(kmeans.inertia_)

plt.plot(range(1,10), inertias, marker='o')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()

# K Means (optimal k = 3)

kmeans = KMeans(n_clusters = 3, random_state = 41)
song_kmeans = song_data_norm.drop(['weighted_score'], axis = 1)
song_kmeans["cluster"] = kmeans.fit_predict(song_data_norm[normalize_col])

cluster_summary = song_kmeans.groupby("cluster")[normalize_col].mean()
cluster_summary

song_kmeans.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Song_KMeans.csv", index = False)
cluster_summary.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Song_Clusters.csv", index = True)





