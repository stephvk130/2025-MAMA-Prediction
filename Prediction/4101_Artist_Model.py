#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephaniechen
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


## Import Data
mg_data = pd.read_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Male_Group_Data.csv")
fg_data = pd.read_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Female_Group_Data.csv")
mg_stream = pd.read_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Male_Group_stream.csv")
fg_stream = pd.read_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Female_Group_stream.csv")


## Add Streaming Weights
mg_data['stream_score'] = int(0)
mg_data.loc[mg_data['artist_name'] == "BOYNEXTDOOR", 'stream_score'] = int(2)
mg_data.loc[(mg_data['artist_name'] == "RIIZE") | (mg_data['artist_name'] == "SEVENTEEN"), 'stream_score'] = int(1)

fg_data['stream_score'] = int(0)
fg_data.loc[fg_data['artist_name'] == "aespa", 'stream_score'] = int(3)
fg_data.loc[fg_data['artist_name'] == "IVE", 'stream_score'] = int(2)
fg_data.loc[(fg_data['artist_name'] == "BABYMONSTER") | (fg_data['artist_name'] == "LE SSERAFIM"), 
            'stream_score'] = int(1)


## Normalize Covariates
norm_col = mg_data.iloc[:, 1:].columns.tolist()

scaler = StandardScaler()
mg_data_norm = mg_data.copy()
mg_data_norm[norm_col] = scaler.fit_transform(mg_data_norm[norm_col])

fg_data_norm = fg_data.copy()
fg_data_norm[norm_col] = scaler.fit_transform(fg_data_norm[norm_col])


## Ranking Model

# Male Group
mg_weights = {'popularity_score': 0.15, 'albums_popularity': 0.15, 'Youtube_views': 0.10, 
              'albums_count': 0.10, 'album_average_sales': 0.20, 'stream_score': 0.30}

mg_data_norm["weighted_score"] = (mg_data_norm["popularity_score"] * mg_weights["popularity_score"] +
                                  mg_data_norm["albums_popularity"] * mg_weights["albums_popularity"] +
                                  mg_data_norm["Youtube_views"] * mg_weights["Youtube_views"] +
                                  mg_data_norm["albums_count"] * mg_weights["albums_count"] +
                                  mg_data_norm["album_average_sales"] * mg_weights["album_average_sales"] +
                                  mg_data_norm["stream_score"] * mg_weights["stream_score"]) 

mg_ranked = mg_data_norm.sort_values("weighted_score", ascending = False)
mg_ranked["rank"] = mg_ranked["weighted_score"].rank(method = "first", ascending = False).astype(int)
mg_ranked.insert(0, "rank", mg_ranked.pop(mg_ranked.columns[-1]))

# Female Group
fg_weights = {'Spotify_followers': 0.10, 'popularity_score': 0.10, 'albums_popularity': 0.10, 'Youtube_views': 0.10, 
              'albums_count': 0.10, 'album_average_sales': 0.20, 'stream_score': 0.30}

fg_data_norm["weighted_score"] = (fg_data_norm["Spotify_followers"] * fg_weights["Spotify_followers"] +
                                  fg_data_norm["popularity_score"] * fg_weights["popularity_score"] +
                                  fg_data_norm["albums_popularity"] * fg_weights["albums_popularity"] +
                                  fg_data_norm["Youtube_views"] * fg_weights["Youtube_views"] +
                                  fg_data_norm["albums_count"] * fg_weights["albums_count"] +
                                  fg_data_norm["album_average_sales"] * fg_weights["album_average_sales"] +
                                  fg_data_norm["stream_score"] * fg_weights["stream_score"]) 

fg_ranked = fg_data_norm.sort_values("weighted_score", ascending = False)
fg_ranked["rank"] = fg_ranked["weighted_score"].rank(method = "first", ascending = False).astype(int)
fg_ranked.insert(0, "rank", fg_ranked.pop(fg_ranked.columns[-1]))


mg_ranked.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Male_Group_Weighted_Rank.csv", index = False)
fg_ranked.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Female_Group_Weighted_Rank.csv", index = False)


## PCA

# Male Group
mg_col = ['popularity_score', 'albums_popularity', 'Youtube_views', 'albums_count', 
          'album_average_sales', 'stream_score']
mg_pca = mg_data_norm[mg_col]

pca = PCA(n_components = 1)
mg_pca_components = pca.fit_transform(mg_pca)

mg_data_pca = mg_data_norm.drop(['weighted_score'], axis = 1)
mg_data_pca["PC1"] = mg_pca_components[:,0]

mg_data_pca = mg_data_pca.sort_values("PC1", ascending = False)
mg_data_pca["rank"] = mg_data_pca["PC1"].rank(method = "first", ascending = False).astype(int)
mg_data_pca.insert(0, "rank", mg_data_pca.pop(mg_data_pca.columns[-1]))

# Female Group
fg_col = ['Spotify_followers', 'popularity_score', 'albums_popularity', 'Youtube_views', 
          'albums_count', 'album_average_sales', 'stream_score']
fg_pca = fg_data_norm[fg_col]

pca = PCA(n_components = 1)
fg_pca_components = pca.fit_transform(fg_pca)

fg_data_pca = fg_data_norm.drop(['weighted_score'], axis = 1)
fg_data_pca["PC1"] = fg_pca_components[:,0]

fg_data_pca = fg_data_pca.sort_values("PC1", ascending = False)
fg_data_pca["rank"] = fg_data_pca["PC1"].rank(method = "first", ascending = False).astype(int)
fg_data_pca.insert(0, "rank", fg_data_pca.pop(fg_data_pca.columns[-1]))


mg_data_pca.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Male_Group_PCA_Rank.csv", index = False)
fg_data_pca.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Female_Group_PCA_Rank.csv", index = False)


## K-Means Clustering

# Male Group Elbow Plot
mg_inertias = []
for k in range(1,8):
    kmeans = KMeans(n_clusters = k, random_state = 41).fit(mg_data_norm[mg_col])
    mg_inertias.append(kmeans.inertia_)

plt.plot(range(1,8), mg_inertias, marker='o')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method - Male Group")
plt.show()

# Male Group K Means (optimal k = 2)
kmeans = KMeans(n_clusters = 2, random_state = 41)
mg_kmeans = mg_data_norm.drop(['weighted_score'], axis = 1)
mg_kmeans["cluster"] = kmeans.fit_predict(mg_data_norm[mg_col])

mg_cluster_summary = mg_kmeans.groupby("cluster")[mg_col].mean()
mg_cluster_summary


# Female Group Elbow Plot
fg_inertias = []
for k in range(1,7):
    kmeans = KMeans(n_clusters = k, random_state = 41).fit(fg_data_norm[fg_col])
    fg_inertias.append(kmeans.inertia_)

plt.plot(range(1,7), fg_inertias, marker='o')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method - Female Group")
plt.show()

# Female Group K Means (optimal k = 3)
kmeans = KMeans(n_clusters = 3, random_state = 41)
fg_kmeans = fg_data_norm.drop(['weighted_score'], axis = 1)
fg_kmeans["cluster"] = kmeans.fit_predict(fg_data_norm[fg_col])

fg_cluster_summary = fg_kmeans.groupby("cluster")[fg_col].mean()
fg_cluster_summary


mg_kmeans.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Male_Group_KMeans.csv", index = False)
fg_kmeans.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Female_Group_KMeans.csv", index = False)
mg_cluster_summary.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Male_Group_Clusters.csv", index = True)
fg_cluster_summary.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Female_Group_Clusters.csv", index = True)








