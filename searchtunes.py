import requests


def findArtist(song_title, album_title):
    base_url = "https://itunes.apple.com/search"
    params = {
        "term": f"{song_title} {album_title}",
        "media": "music",
        "entity": "musicTrack",
        "limit": 1
    }

    try:
        response = requests.get(base_url, params=params)
    except:
        print('uh oh')
    response.raise_for_status()

    data = response.json()
    results = data.get('results', [])

    if results:
        artist_name = results[0].get('artistName', 'Artist not found')
        return artist_name
    else:
        return "No results found"



