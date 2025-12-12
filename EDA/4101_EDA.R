### STA 4101 Final Project EDA

library(dplyr)
library(ggplot2)
library(tidyr)
library(corrplot)
library(zoo)

## Import Data
song_data <- read.csv("Project_Song_Data.csv", header = TRUE)
male_trend <- read.csv("Project_Male_Group_Trend_Data.csv", header = TRUE)
female_trend <- read.csv("Project_Female_Group_Trend_Data.csv", header = TRUE)
male_group <- read.csv("Project_Male_Group_Data.csv", header = TRUE)
female_group <- read.csv("Project_Female_Group_Data.csv", header = TRUE)
male_stream <- read.csv("Project_Male_Group_Stream.csv", header = TRUE)
female_stream <- read.csv("Project_Female_Group_Stream.csv", header = TRUE)


## Song Data
song_data$interaction_ratio <- (song_data$mv_like_count + song_data$mv_comment_count) / song_data$mv_view_count

# Scatter Plot
song_plot1 <- ggplot(song_data, aes(x = interaction_ratio, y = popularity_score)) +
  geom_point(size = 1.8, shape = 16, color = "darkblue", alpha = 0.9) +
  geom_text(aes(label = song_name), vjust = -0.6, size = 2.5, color = "black") +
  labs(title = "Spotify Popularity VS Youtube Interaction",
       x = "Interaction Ratio",
       y = "Popularity Score") +
  theme_minimal() +             
  theme(plot.title = element_text(hjust = 0.5))  
song_plot1

# Top 5 Songs
metric_cols <- song_data %>% select(where(is.numeric)) %>% colnames()
top5_songs <- data.frame(rank = 1:5)

for (col in metric_cols) {
  ordered_idx <- order(song_data[[col]], decreasing = TRUE)
  top5_song <- song_data$song_name[ordered_idx][1:5]
  top5_songs[[col]] <- top5_song
}

top5_songs


## Google Trend Data
# Male Group
male_trend$date <- as.Date(male_trend$date)
male_trend_long <- pivot_longer(male_trend, cols = -date, 
                                names_to = "group", values_to = "trend_score")

ggplot(male_trend_long, aes(x = date, y = trend_score, color = group)) +
  geom_line(linewidth = 1.1) +
  scale_color_manual(
    values = c("#C06D6D", "#457B9D", "#2A9D8F", "#E9C46A", 
               "#C07D54", "#9689B1", "#D8A8B8"),
    name = "Groups",
    labels = c("SEVENTEEN", "TOMORROW X TOGETHER", "BOYNEXTDOOR", 
               "ENHYPEN", "RIIZE", "Stray Kids", "ZEROBASEONE")) +
  labs(x = "Date", y = "Trend Score") +
  theme_minimal()

# Female Group
female_trend$date <- as.Date(female_trend$date)
female_trend_long <- pivot_longer(female_trend, cols = -date, 
                                names_to = "group", values_to = "trend_score")

ggplot(female_trend_long, aes(x = date, y = trend_score, color = group)) +
  geom_line(linewidth = 1.1) +
  scale_color_manual(
    values = c("#C06D6D", "#457B9D", "#2A9D8F", "#E9C46A", "#D8A8B8", "#9689B1"),
    name = "Groups",
    labels = c("aespa", "BABYMONSTER", "i-dle", "IVE", "LE SSERAFIM", "TWICE")) +
  labs(x = "Date", y = "Trend Score") +
  theme_minimal()


## Group Data
# Male Group 
# Heat Map
male_group_num <- male_group %>% select(where(is.numeric))
male_group_cor_matrix <- cor(male_group_num, use = "complete.obs")
print(male_group_cor_matrix)

male_group_heatmap <- corrplot(male_group_cor_matrix, method = "color", type = "upper", order = "hclust",
                               tl.col = "black", tl.srt = 45, addCoef.col = "black", number.cex = 0.8, 
                               col = colorRampPalette(c("lemonchiffon2", "white", "lavenderblush3"))(100),
                               main = "Male Group Metrics Correlation Heatmap", mar = c(0, 0, 2, 0))
male_group_heatmap

# Scatter Plot: Popularity Score vs Average Album Sales
male_group_plot1 <- ggplot(male_group, aes(x = popularity_score, y = album_average_sales)) +
  geom_point(size = 5, color = "brown", alpha = 0.8) +
  geom_text(aes(label = paste(artist_name)), vjust = -1.2, size = 2.8, check_overlap = TRUE) +
  scale_x_continuous(limits = c(50, 100)) + 
  labs(title = "Male Group Nominees Scatter Plot",
       subtitle = "Popularity Score vs Average Album Sales", 
       x = "Popularity Score",
       y = "Average Album Sales") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 11),
        legend.position = "none") 
male_group_plot1

# Top 2 Groups
mg_metric_cols <- male_group %>% select(-artist_name, -album_sales, -albums_count) %>% colnames()
top2_male_groups <- data.frame(rank = 1:2)

for (col in mg_metric_cols) {
  ordered_idx <- order(male_group[[col]], decreasing = TRUE)
  top2_mg <- male_group$artist_name[ordered_idx][1:2]
  top2_male_groups[[col]] <- top2_mg
}

top2_male_groups


# Female Group
# Heat Map
female_group_num <- female_group %>% select(where(is.numeric))
female_group_cor_matrix <- cor(female_group_num, use = "complete.obs")
print(female_group_cor_matrix)

female_group_heatmap <- corrplot(female_group_cor_matrix, method = "color", type = "upper", order = "hclust",
                                 tl.col = "black", tl.srt = 45, addCoef.col = "black", number.cex = 0.8, 
                                 col = colorRampPalette(c("lemonchiffon2", "white", "lavenderblush3"))(100),
                                 main = "Female Group Metrics Correlation Heatmap", mar = c(0, 0, 2, 0))
female_group_heatmap

# Scatter Plot: Popularity Score vs Average Album Sales
female_group_plot1 <- ggplot(female_group, aes(x = popularity_score, y = album_average_sales)) +
  geom_point(size = 5, color = "brown", alpha = 0.8) +
  geom_text(aes(label = paste(artist_name)), vjust = -1.2, size = 2.8, check_overlap = TRUE) +
  scale_x_continuous(limits = c(50, 100)) + 
  labs(title = "Female Group Nominees Scatter Plot",
       subtitle = "Popularity Score vs Average Album Sales", 
       x = "Popularity Score",
       y = "Average Album Sales") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 11),
        legend.position = "none") 
female_group_plot1

# Top 2 Groups
fg_metric_cols <- female_group %>% select(-artist_name, -album_sales, -albums_count) %>% colnames()
top2_female_groups <- data.frame(rank = 1:2)

for (col in fg_metric_cols) {
  ordered_idx <- order(female_group[[col]], decreasing = TRUE)
  top2_fg <- female_group$artist_name[ordered_idx][1:2]
  top2_female_groups[[col]] <- top2_fg
}

top2_female_groups


## Stream Data
# Male Group
mg_stream_long <- male_stream %>%
  pivot_longer(cols = 'X2024.10':'X2025.9', names_to = "month", values_to = "streams") %>%
  mutate(month_clean = gsub("^X", "", month), 
         month_ym = as.yearmon(month_clean, format = "%Y.%m"),
         artist_song = paste(artist_name, song_name, sep = ": "),)

mg_stream_plot <- ggplot(mg_stream_long %>% filter(streams != 0),
                         aes(x = month_ym, y = streams, color = artist_song, group = artist_song)) +
  geom_line(linewidth = 1, alpha = 0.9) +
  geom_point(size = 1, alpha = 0.7) +
  geom_text(aes(label = streams), vjust = -0.8, size = 3, color = "black", show.legend = FALSE) +
  scale_x_yearmon(format = "%Y.%m") + 
  scale_y_reverse(limits = c(100, 0)) +
  scale_color_brewer(palette = "Dark2", name = "Song") +
  labs(title = "Male Group Monthly Streaming Rank", x = "Month", y = "Stream Rank") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        axis.text.x = element_text(angle = 45, hjust = 1),
        legend.title = element_text(face = "bold", color = "black"),
        legend.text = element_text(color = "black"))
mg_stream_plot

# Female Group
fg_stream_long <- female_stream %>%
  pivot_longer(cols = 'X2024.10':'X2025.9', names_to = "month", values_to = "streams") %>%
  mutate(month_clean = gsub("^X", "", month), 
         month_ym = as.yearmon(month_clean, format = "%Y.%m"),
         artist_song = paste(artist_name, song_name, sep = ": "),)

fg_stream_plot <- ggplot(fg_stream_long %>% filter(streams != 0),
                         aes(x = month_ym, y = streams, color = artist_song, group = artist_song)) +
  geom_line(linewidth = 1, alpha = 0.9) +
  geom_point(size = 1, alpha = 0.7) +
  geom_text(aes(label = streams), vjust = -0.8, size = 3, color = "black", show.legend = FALSE) +
  scale_x_yearmon(format = "%Y.%m") + 
  scale_y_reverse(limits = c(100, 0)) +
  scale_color_brewer(palette = "Paired", name = "Song") +
  labs(title = "Female Group Monthly Streaming Rank", x = "Month", y = "Stream Rank") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, face = "bold"),
        axis.text.x = element_text(angle = 45, hjust = 1),
        legend.title = element_text(face = "bold", color = "black"),
        legend.text = element_text(color = "black"))
fg_stream_plot





