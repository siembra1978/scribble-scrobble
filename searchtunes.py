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
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])

        if results:
            artist_name = results[0].get('artistName', 'Artist not found')
            return artist_name
        else:
            return "No results found"
    except requests.exceptions.HTTPError as err:
        # Handle specific errors from HTTP responses (e.g., 404, 503)
        print("ruh roh")
        return "No results found"
    except requests.exceptions.ConnectionError:
        # Handle errors like DNS failure, refused connection
        print("ruh roh")
        return "No results found"
    except requests.exceptions.Timeout:
        # Handle timeouts
        print("ruh roh")
        return "No results found"
    except requests.exceptions.RequestException as e:
        # Handle any requests-related errors
        print("ruh roh")
        return "No results found"
    except Exception as e:
        # Handle other unforeseen errors
        print("ruh roh")
        return "No results found"



