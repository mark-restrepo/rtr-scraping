import json
import time

import requests
import os

spotify_key = os.environ['SPOTIFY_KEY']


def get_spotify_id(artist: str):
    time.sleep(1)
    try:
        r = requests.get(f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1",
                         headers={"Authorization": f"Bearer {spotify_key}"})
        result = json.loads(r.content)
        return result['artists']['items'][0]['id']
    except Exception as e:
        print(f"Spotify ID retrieval failed for {artist}: {e}")
        return None
