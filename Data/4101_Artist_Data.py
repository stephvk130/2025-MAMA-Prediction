#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephaniechen
"""

import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from pytrends.request import TrendReq

best_male_list = ["SEVENTEEN", "TOMORROW X TOGETHER", "BOYNEXTDOOR", "ENHYPEN", "RIIZE", "Stray Kids", "ZEROBASEONE"]
best_female_list = ["aespa", "BABYMONSTER", "i-dle", "IVE", "LE SSERAFIM", "TWICE"]
best_male_df = pd.DataFrame(columns = ["artist_name", "Spotify_followers", "popularity_score", "albums_popularity",
                                       "Youtube_subscribers", "Youtube_views"])
best_female_df = pd.DataFrame(columns = ["artist_name", "Spotify_followers", "popularity_score", "albums_popularity",
                                         "Youtube_subscribers", "Youtube_views"])


# Spotify API
	
client_id = "35ce50e2ebfa41f6aab41206c30dab84"
client_secret = "72e5317f165545c8ace7109df9517a0c"

sp = spotipy.Spotify(
    auth_manager = SpotifyClientCredentials(
        client_id = client_id,                                            
        client_secret = client_secret
    )
)

def album_popularity_sum(artist_name, start_date = "2024-10-01", end_date = "2025-09-30"):

    results = sp.search(q = f'artist:{artist_name}', type = "artist", limit = 1)
    items = results["artists"]["items"]
    if len(items) == 0:
        return 0
    
    artist_id = items[0]["id"]
    
    albums = []
    results = sp.artist_albums(artist_id, album_type = "album,single,appears_on,compilation", 
                               country = "US", limit = 50)
    while results:
        for album in results["items"]:
            release_date = album["release_date"]
            if len(release_date) == 4:
                release_date = release_date + "-01-01"
            elif len(release_date) == 7:
                release_date = release_date + "-01"
            if start_date <= release_date <= end_date:
                albums.append(album["id"])
        if results["next"]:
            results = sp.next(results)
        else:
            break
    
    total_pop = 0
    for album_id in albums:
        tracks = sp.album_tracks(album_id)["items"]
        track_ids = [t["id"] for t in tracks]
        if not track_ids:
            continue
        track_infos = sp.tracks(track_ids)["tracks"]
        popularities = [t["popularity"] for t in track_infos]
        if popularities:
            total_pop = total_pop + sum(popularities)
    
    return total_pop

# Male Group

for i in range(len(best_male_list)):
    result = sp.search(q = f'artist:{best_male_list[i]}', type = "artist", limit = 1)
    items = result["artists"]["items"]
    if len(items) == 0:
        print(f"Artist not found: {best_male_list[i]}")
        continue
    pop_score = album_popularity_sum(best_male_list[i])
    
    artist = items[0]
    best_male_df.loc[i, "artist_name"] = artist["name"]
    best_male_df.loc[i, "Spotify_followers"] = artist["followers"]["total"]
    best_male_df.loc[i, "popularity_score"] = artist["popularity"]
    best_male_df.loc[i, "albums_popularity"] = pop_score
    time.sleep(5)
       
# Female Group

for i in range(len(best_female_list)):
    result = sp.search(q = f'artist:{best_female_list[i]}', type = "artist", limit = 1)
    items = result["artists"]["items"]
    if len(items) == 0:
        print(f"Artist not found: {best_female_list[i]}")
        continue
    pop_score = album_popularity_sum(best_female_list[i])
    
    artist = items[0]
    best_female_df.loc[i, "artist_name"] = artist["name"]
    best_female_df.loc[i, "Spotify_followers"] = artist["followers"]["total"]
    best_female_df.loc[i, "popularity_score"] = artist["popularity"]
    best_female_df.loc[i, "albums_popularity"] = pop_score
    time.sleep(5)
 
# Revise Data

ive_id = "6RHTUrRF63xao58xh9FXYJ"
artist_ive = sp.artist(ive_id)

best_female_df.loc[3, "artist_name"] = artist_ive["name"]
best_female_df.loc[3, "Spotify_followers"] = artist_ive["followers"]["total"]
best_female_df.loc[3, "popularity_score"] = artist_ive["popularity"]

ive_albums = []
ive_results = sp.artist_albums(ive_id, album_type = "album,single,appears_on,compilation", 
                               country = "US", limit = 50)
while ive_results:
    for album in ive_results["items"]:
        release_date = album["release_date"]
        if len(release_date) == 4:
            release_date = release_date + "-01-01"
        elif len(release_date) == 7:
            release_date = release_date + "-01"
        if "2024-10-01" <= release_date <= "2025-09-30":
            ive_albums.append(album["id"])
    if ive_results["next"]:
        ive_results = sp.next(ive_results)
    else:
        break

ive_pop = 0
for album_id in ive_albums:
    ive_tracks = sp.album_tracks(album_id)["items"]    
    ive_track_ids = [t["id"] for t in ive_tracks]
    ive_track_infos = sp.tracks(ive_track_ids)["tracks"]
    ive_popularities = [t["popularity"] for t in ive_track_infos]
    if ive_popularities:
        ive_pop = ive_pop + sum(ive_popularities)

best_female_df.loc[3, "albums_popularity"] = ive_pop



# Youtube API

youtube_api_key = "AIzaSyDvOi3ETXAsmLSqIP6jMahBZGCe41UTNI8"
youtube = build("youtube", "v3", developerKey = youtube_api_key)

best_male_yt_id = ["UCfkXDY7vwkcJ8ddFGz8KusA", "UCtiObj3CsEAdNU6ZPWDsddQ", "UChhKBlh_wvspTh5n4mL0b5g",
                   "UCArLZtok93cO5R9RI4_Y5Jw", "UCdVD0MsYecQaIE5Ru-pOIQQ", "UC9rMiEjNaCSsebs31MRDCRA",
                   "UCSAp0Yl9S0Zq5uDqE6im_XQ"]
best_female_yt_id = ["UC9GtSLeksfK4yuJ_g1lgQbg", "UCqwUnggBBct-AY2lAdI88jQ", "UCritGVo7pLJLUS8wEu32vow",
                     "UC-Fnix71vRP64WXeo0ikd0Q", "UCs-QBT4qkj_YiQw1ZntDO3g", "UCzgxx_DM2Dcb9Y1spb9mUJA"]

def get_channel_statistics(channel_id):
    request = youtube.channels().list(part = "statistics", id = channel_id)
    response = request.execute()
    stats = response["items"][0]["statistics"]
    subscribers = int(stats.get("subscriberCount", 0))
    total_views = int(stats.get("viewCount", 0))
    return subscribers, total_views

# Male Group

for i in range(len(best_male_yt_id)):
    male_channel_id = best_male_yt_id[i]
    male_channel_stats = get_channel_statistics(male_channel_id)
    
    best_male_df.loc[i, "Youtube_subscribers"] = male_channel_stats[0]
    best_male_df.loc[i, "Youtube_views"] = male_channel_stats[1]
    time.sleep(1)
    
# Female Group

for i in range(len(best_female_yt_id)):
    female_channel_id = best_female_yt_id[i]
    female_channel_stats = get_channel_statistics(female_channel_id)
    
    best_female_df.loc[i, "Youtube_subscribers"] = female_channel_stats[0] 
    best_female_df.loc[i, "Youtube_views"] = female_channel_stats[1]  
    time.sleep(1)    


best_male_df[["Spotify_followers", "popularity_score", "albums_popularity", "Youtube_subscribers", 
              "Youtube_views"]] = best_male_df[["Spotify_followers", "popularity_score", "albums_popularity", 
                                                "Youtube_subscribers", "Youtube_views"]].astype(int)
best_female_df[["Spotify_followers", "popularity_score", "albums_popularity", "Youtube_subscribers", 
              "Youtube_views"]] = best_female_df[["Spotify_followers", "popularity_score", "albums_popularity", 
                                                "Youtube_subscribers", "Youtube_views"]].astype(int)


                                                  
# Circle Chart Data

# Male Group

best_male_df['album_sales'] = int(0)
best_male_df.loc[0, 'album_sales'] = int(2545862)
best_male_df.loc[1, 'album_sales'] = int(3550765)
best_male_df.loc[2, 'album_sales'] = int(1166922)
best_male_df.loc[3, 'album_sales'] = int(3482378)
best_male_df.loc[4, 'album_sales'] = int(1413171)
best_male_df.loc[5, 'album_sales'] = int(5463232)
best_male_df.loc[6, 'album_sales'] = int(2743661)

best_male_df['albums_count'] = int(2)
best_male_df.loc[0, 'albums_count'] = int(1)
best_male_df.loc[2, 'albums_count'] = int(1)
best_male_df.loc[4, 'albums_count'] = int(1)

best_male_df['album_average_sales'] = best_male_df['album_sales'].astype(int)
best_male_df.loc[1, 'album_average_sales'] = int(best_male_df.loc[1, 'album_sales'] / 2)
best_male_df.loc[3, 'album_average_sales'] = int(best_male_df.loc[3, 'album_sales'] / 2)
best_male_df.loc[5, 'album_average_sales'] = int(best_male_df.loc[5, 'album_sales'] / 2)
best_male_df.loc[6, 'album_average_sales'] = int(best_male_df.loc[6, 'album_sales'] / 2)

# Female Group

best_female_df['album_sales'] = int(0)
best_female_df.loc[0, 'album_sales'] = int(2118968)
best_female_df.loc[1, 'album_sales'] = int(418581)
best_female_df.loc[3, 'album_sales'] = int(2432092)
best_female_df.loc[4, 'album_sales'] = int(689600)
best_female_df.loc[5, 'album_sales'] = int(1621147)

best_female_df['albums_count'] = int(2)
best_female_df.loc[1, 'albums_count'] = int(1)
best_female_df.loc[2, 'albums_count'] = int(0)
best_female_df.loc[4, 'albums_count'] = int(1)

best_female_df['album_average_sales'] = best_female_df['album_sales'].astype(int)
best_female_df.loc[0, 'album_average_sales'] = int(best_female_df.loc[0, 'album_sales'] / 2)
best_female_df.loc[3, 'album_average_sales'] = int(best_female_df.loc[3, 'album_sales'] / 2)
best_female_df.loc[5, 'album_average_sales'] = int(best_female_df.loc[5, 'album_sales'] / 2)

                                                  
best_male_df.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Male_Group_Data.csv", index = False)
best_female_df.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Female_Group_Data.csv", index = False)


# Streaming Rank

stream_col = ['artist_name', 'album_name', 'song_name', '2024.10', '2024.11', '2024.12', '2025.1', '2025.2', 
              '2025.3', '2025.4', '2025.5', '2025.6', '2025.7', '2025.8', '2025.9']


best_male_stream = pd.DataFrame([
    ['SEVENTEEN', 'HAPPY BURSTDAT', 'THUNDER', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(0), int(30), int(72), int(88), int(0)],
    ['BOYNEXTDOOR', 'No Genre', 'IF I SAY, I LOVE YOU', int(0), int(0), int(0), int(18), 
     int(7), int(9), int(10), int(8), int(10), int(26), int(24), int(39)],
    ['BOYNEXTDOOR', 'No Genre', 'I Feel Good', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(87), int(75), int(0), int(0), int(0)],   
    ['BOYNEXTDOOR', 'No Genre', '123-78', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(85), int(40), int(64), int(86), int(0)], 
    ['RIIZE', 'ODYSSEY', 'Fly Up', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(98), int(59), int(88), int(94), int(0)]
    ], columns = stream_col)


best_female_stream = pd.DataFrame([
    ['aespa', 'Whiplash', 'Whiplash', int(25), int(2), int(3), int(3), 
     int(3), int(6), int(5), int(5), int(7), int(10), int(11), int(11)], 
    ['aespa', 'Rich Man', 'Rich Man', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(6)],
    ['BABYMONSTER', 'DRIP', 'DRIP', int(0), int(54), int(34), int(13), 
     int(12), int(18), int(28), int(32), int(39), int(52), int(59), int(68)],
    ['IVE', 'IVE EMPATHY', 'REBEL HEART', int(0), int(0), int(0), int(24), 
     int(1), int(5), int(8), int(11), int(18), int(30), int(30), int(38)],
    ['IVE', 'IVE EMPATHY', 'ATTITUDE', int(0), int(0), int(0), int(0), 
     int(11), int(11), int(15), int(19), int(32), int(51), int(64), int(69)],
    ['IVE', 'IVE SECRET', 'XOXZ', int(0), int(0), int(0), int(0), 
     int(0), int(0), int(0), int(0), int(0), int(0), int(0), int(7)],
    ['LE SSERAFIM', 'HOT', 'HOT', int(0), int(0), int(0), int(0), 
     int(0), int(65), int(11), int(13), int(22), int(38), int(53), int(62)]      
    ], columns = stream_col)


best_male_stream.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Male_Group_Stream.csv", index = False)
best_female_stream.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Female_Group_Stream.csv", index = False)



# Google Trend API

pytrends = TrendReq(hl='en-US', tz=360)

time_frame = "2024-10-01 2025-09-30"
trend_data_male_group = pd.DataFrame()
trend_data_female_group = pd.DataFrame()

for male_group in best_male_list:

    pytrends.build_payload([male_group], timeframe = time_frame)
    df_male = pytrends.interest_over_time()

    if df_male.empty:
        print(f"No trend data for: {male_group}")
        continue

    df_male = df_male.drop(columns=["isPartial"], errors="ignore")
    df_male.rename(columns={male_group: male_group.replace(" ", "_")}, inplace=True)

    if trend_data_male_group.empty:
        trend_data_male_group = df_male
    else:
        trend_data_male_group = trend_data_male_group.join(df_male, how="outer")
    time.sleep(20)


for female_group in best_female_list:

    pytrends.build_payload([female_group], timeframe = time_frame)
    df_female = pytrends.interest_over_time()

    if df_female.empty:
        print(f"No trend data for: {female_group}")
        continue

    df_female = df_female.drop(columns=["isPartial"], errors="ignore")
    df_female.rename(columns={female_group: female_group.replace(" ", "_")}, inplace=True)

    if trend_data_female_group.empty:
        trend_data_female_group = df_female
    else:
        trend_data_female_group = trend_data_female_group.join(df_female, how="outer")
    time.sleep(20)

trend_data_male_group.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Male_Group_Trend_Data.csv",
                             index = True)
trend_data_female_group.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Female_Group_Trend_Data.csv",
                               index = True)




