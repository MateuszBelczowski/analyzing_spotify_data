import json

import musicbrainzngs

musicbrainzngs.set_useragent("Live hacking app", "0.0.1", "")

with open("data/StreamingHistory1.json", encoding="utf-8") as f:
    data = json.load(f)
    
for entry in data:
    result = musicbrainzngs.search_artists(artist=entry['artistName'])
    try:
        tags = result['artist-list'][0]['tag-list']
        print(tags)
    except (KeyError, IndexError) as e:
        print(entry["artistName"], e)