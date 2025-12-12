#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephaniechen
"""

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build


song_list = ["aespa Dirty Work", "aespa Whiplash", "ALLDAY PROJECT FAMOUS", "ALLDAY PROJECT WICKED",
             "BABYMONSTER DRIP", "BIG Naughty MUSIC", "BLACKPINK JUMP", "BOYNEXTDOOR IF I SAY,I LOVE YOU",
             "BOYNEXTDOOR Never Loved This Way Before", "CNBLUE A Sleepless Night", "CORTIS GO!", 
             "DAVICHI Stitching", "DAY6 Maybe Tomorrow", "Dayoung body", "Doyoung Memory", 
             "Dynamicduo GUMMY Take Care", "G-DRAGON Anderson .Paak TOO BAD", "HAON GISELLE Skrr",
             "HIGHLIGHT Endless Ending", "HUNTR/X EJAE AUDREY NUNA REI AMI GOLDEN", "ILLIT Cherish (My Love)",
             "IVE REBEL HEART", "j-hope MONA LISA", "JENNIE like JENNIE", "JENNIE ZEN", "JENNIE Doechii ExtraL",
             "JISOO earthquake", "KAI Wait On Me", "aespa UP - KARINA Solo", "KEY HUNTER", "LE SSERAFIM HOT",
             "LEE CHANHYUK Vivid LaLa Love", "LEE MU JIN Coming Of Age Story", "MARK 1999", "MARK Fraktsiya",
             "MEOVV DROP TOP", "Minnie HER", "N.Flying Everlasting", "NCT DREAM When I'm With You", 
             "NCT WISH poppop", "Park Hyo Shin HERO", "pH-1 Life Is A Movie", "PLAVE Dash", "QWER Dear",
             "RIIZE Fly Up", "ROSE toxic till the end", "ROSE Bruno Mars APT.", "Roy Kim If You Ask Me What Love Is",
             "Saja Boys Andrew Choi Neckwav Danny Chung KEVIN WOO samUIL Lee Soda Pop", "SEVENTEEN THUNDER",
             "TABLO RM Stop The Rain", "TAEYEON Letter To Myself", "TREASURE YELLOW", "TWS Countdown!",
             "TOMORROW X TOGETHER When the Day Comes", "V Winter Ahead", "Xdinary Heroes Beautiful Life",
             "ZEROBASEONE Doctor!Doctor!"]

song_df = pd.DataFrame(columns = ["song_name", "artist_name", "popularity_score", "mv_view_count", "mv_like_count",
                                  "mv_comment_count"])


# Spotify API

client_id = "35ce50e2ebfa41f6aab41206c30dab84"
client_secret = "72e5317f165545c8ace7109df9517a0c"

sp = spotipy.Spotify(
    auth_manager = SpotifyClientCredentials(
        client_id = client_id,                                            
        client_secret = client_secret
    )
)


for i in range(len(song_list)):
    result = sp.search(q = song_list[i], type = "track", limit = 1)
    track = result["tracks"]["items"][0]
    
    track_id = track["id"]
    track_name = track["name"]
    artist_name = track["artists"][0]["name"]
    popu_score = track["popularity"]
    
    song_df.loc[i, "song_name"] = track_name
    song_df.loc[i, "artist_name"] = artist_name
    song_df.loc[i, "popularity_score"] = popu_score

# Youtube API

youtube_api_key = "AIzaSyCjaGOIM4X_THhBN8gtCdXbEdKZN3AgU-A"
youtube = build("youtube", "v3", developerKey = youtube_api_key)


def get_official_mv(song_info):

    request = youtube.search().list(
        q = song_info,
        part = "snippet",
        type = "video",
        maxResults = 10,
        videoCategoryId = "10"  
    )
    response = request.execute()
    
    official_keywords = ["official mv", "official music video", "music video", "mv", "m/v"]
    mv_search = []
    
    for item in response["items"]:
        title = item["snippet"]["title"].lower()
        channel = item["snippet"]["channelTitle"].lower()
        video_id = item["id"]["videoId"]

        if any(k in title for k in official_keywords):
            mv_search.append((video_id, title, channel))
 
    if mv_search:
        return mv_search[0][0] 

    return response["items"][0]["id"]["videoId"]


def get_video_stats(video_id):
    request = youtube.videos().list(
        part = "statistics",
        id = video_id
    )
    response = request.execute()
    stats = response["items"][0]["statistics"]

    return {"views": int(stats.get("viewCount", 0)), "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0))}


for i in range(len(song_list)):
    song_info = song_list[i]
    video_id = get_official_mv(song_info)
    video_stats = get_video_stats(video_id)
    
    song_df.loc[i, "mv_view_count"] = video_stats["views"]
    song_df.loc[i, "mv_like_count"] = video_stats["likes"] 
    song_df.loc[i, "mv_comment_count"] = video_stats["comments"]     


# Data Cleaning

song_df[["popularity_score", "mv_view_count", "mv_like_count","mv_comment_count"]] = song_df[["popularity_score", 
                    "mv_view_count", "mv_like_count","mv_comment_count"]].astype(int)

# Correct MV View Count

wicked_id = "mhKCRnUKp5U"
drip_id = "Zp-Jhuhq0bQ"
never_loved_id = "NeFNFHF1Fzc"
a_sleepless_id = "ai2Afs604_w"
too_bad_id = "o9DhvbqYzns"
endless_id = "jdFtKivrwtY"
golden_id = "yebNIHKAC4A"
extral_id = "eWAdpUyzCkI"
up_id = "U1_0Vc-9mNw"
coming_of_id = "1bZNp9d7pLM"
everlasting_id = "2L_W8hPpdhg"
dash_id = "b3GoZMfHJT4"
soda_pop_id = "983bBbJx0Mk"
yellow_id = "R55VGD7aYUI"
doctor_id = "9BXF8gSpEwY"

revise_song_name = ["WICKED", "DRIP", "Never Loved This Way Before", "A Sleepless Night", "TOO BAD", "Endless Ending",
                    "Golden", "ExtraL (feat. Doechii)", "UP - KARINA Solo", "Coming Of Age Story", "Everlasting",
                    "Dash", "Soda Pop", "YELLOW", "Doctor! Doctor!"]

revise_id_list = [wicked_id, drip_id, never_loved_id, a_sleepless_id, too_bad_id, endless_id, golden_id, extral_id,
                  up_id, coming_of_id, everlasting_id, dash_id, soda_pop_id, yellow_id, doctor_id]


for i in range(len(revise_song_name)):
    revise_video_stats = get_video_stats(revise_id_list[i])
    
    song_df.loc[song_df["song_name"] == revise_song_name[i], "mv_view_count"] = revise_video_stats["views"]
    song_df.loc[song_df["song_name"] == revise_song_name[i], "mv_like_count"] = revise_video_stats["likes"] 
    song_df.loc[song_df["song_name"] == revise_song_name[i], "mv_comment_count"] = revise_video_stats["comments"] 

    
song_df.to_csv("/Users/stephaniechen/Desktop/STA 4101H/Project_Song_Data.csv", index = False)





