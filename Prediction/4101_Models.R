### Only for song prediction model dataframe screenshot

song_weighted_rank <- read.csv("Song_Weighted_Rank.csv", header = TRUE)
song_pca_rank <- read.csv("Song_PCA_Rank.csv", header = TRUE)
song_kmeans <- read.csv("Song_KMeans.csv", header = TRUE)
song_clusters <- read.csv("Song_Clusters.csv", header = TRUE)

# Filter cluster 1
song_cluster1 <- song_kmeans[song_kmeans$cluster == 1, ]


mg_weighted_rank <- read.csv("Male_Group_Weighted_Rank.csv", header = TRUE)
fg_weighted_rank <- read.csv("Female_Group_Weighted_Rank.csv", header = TRUE)
mg_pca_rank <- read.csv("Male_Group_PCA_Rank.csv", header = TRUE)
fg_pca_rank <- read.csv("Female_Group_PCA_Rank.csv", header = TRUE)
mg_kmeans <- read.csv("Male_Group_KMeans.csv", header = TRUE)
fg_kmeans <- read.csv("Female_Group_KMeans.csv", header = TRUE)
mg_clusters <- read.csv("Male_Group_Clusters.csv", header = TRUE)
fg_clusters <- read.csv("Female_Group_Clusters.csv", header = TRUE)

# Weighted rank model display
mg_wr_display <- mg_weighted_rank[, c("rank", "artist_name", "weighted_score")]
fg_wr_display <- fg_weighted_rank[, c("rank", "artist_name", "weighted_score")]

# PCA display
mg_pca_display <- mg_pca_rank[, c("rank", "artist_name", "PC1")]
fg_pca_display <- fg_pca_rank[, c("rank", "artist_name", "PC1")]

# Filter group clusters
mg_cluster0 <- mg_kmeans[mg_kmeans$cluster == 0, ]
mg_cluster1 <- mg_kmeans[mg_kmeans$cluster == 1, ]

fg_cluster0 <- fg_kmeans[fg_kmeans$cluster == 0, ]
fg_cluster1 <- fg_kmeans[fg_kmeans$cluster == 1, ]



