import os
import PyPDF2
import json
import traceback

def get_table_data(music_str):
    try:
        ##converting the music list from a str to dict
        print(f"Debug: Music string to decode: {music_str}")
        if music_str.startswith("###RESPONSE_JSON "):
            music_str = music_str[len("###RESPONSE_JSON "):]
        music_dict = json.loads(music_str)
        music_table_data= []
        for key in music_dict["songs"]:
            title = key["title"]
            movie = key["movie"]
            year = key["year"]
            #music_table_data.append({"Title": title, "Movie": movie, "Year": year})
            music_table_data.append({"Title": title, "Movie": movie, "Year": year})
        #formatted_music_list = " | ".join([f"Title: {song['Title']}, Movie: {song['Movie']}, Year: {song['Year']}" for song in music_table_data])
        return music_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


