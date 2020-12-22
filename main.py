import json
from urllib.parse import urlencode

import requests

with open("data/StreamingHistory1.json", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))

ms_per_artist = {}
for entry in data:
    artist_name = entry["artistName"]
    if artist_name in ms_per_artist:
        ms_per_artist[artist_name] += entry["msPlayed"]
    else:
        ms_per_artist[artist_name] = entry["msPlayed"]

print(ms_per_artist)
print(len(ms_per_artist))

sorted_dict = {artist: ms_played for artist, ms_played in sorted(ms_per_artist.items(), key=lambda item: item[1], reverse=True)}

for artist in sorted_dict:
    print(f"{artist} -> {round(sorted_dict[artist] / 1000 / 60, 2)} minutes")
    
url = "https://itunes.apple.com/search?"


chars_to_remove = "!.&-',?/\\\"+:()"
dead_letter_queue = []

for idx, entry in enumerate(data):
    print(idx)
    query_term = entry['artistName'] + " " + entry['trackName']
    query_term = query_term.lower()
    for char in chars_to_remove:
        query_term = query_term.replace(char, "")
    queryparam = urlencode({"term": query_term})
    response = requests.get(url + queryparam)
    if response.status_code != 200:
        dead_letter_queue.append(entry)
        print(response.status_code)
        print(queryparam)
        print(response.headers)
        continue
    results = response.json()['results']
    if len(results):
        print(query_term)
        print(results[0]["primaryGenreName"])


print(dead_letter_queue)

