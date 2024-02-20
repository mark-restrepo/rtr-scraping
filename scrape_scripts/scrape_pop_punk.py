import time

import numpy as np
import requests
import tqdm
from bs4 import BeautifulSoup
import pandas as pd

from rtr import Artist
from rtr.origin import get_origin, get_birthplace

r = requests.get("https://en.wikipedia.org/wiki/List_of_pop-punk_bands")

soup = BeautifulSoup(r.content, "html.parser")

add_to_list = False

artists = []
for entry in soup.find_all('li'):
    if entry.find("a"):
        if entry.find("a").get('href'):
            entry_text = entry.get_text().split('[')[0]
            if entry_text == "+44":
                add_to_list = True
            if add_to_list:
                a = Artist(entry_text)
                a.link = entry.find("a").get('href')
                artists.append(a)
            if entry_text == "Zolof the Rock and Roll Destroyer":
                add_to_list = False

for artist in tqdm.tqdm(artists):
    # time.sleep(0.1)
    content = requests.get("https://en.wikipedia.org" + artist.link).content
    artist.origin = get_origin(content)
    artist.birth = get_birthplace(content)

df = pd.DataFrame(
    [(a.name, a.link, a.origin, a.birth) for a in artists],
    columns=["name", "link", "origin", "birth"]
)
df['birth'] = df.birth.replace({np.nan: None})
df['origin'] = df.origin.replace({np.nan: None})

df = df[~df.origin.isnull() | ~df.birth.isnull()]
#
# df["origin_point"] = df["origin"].apply(geocode)
# df["birth_point"] = df["birth"].apply(geocode)
#
# df['spotify_id'] = df["name"].apply(get_spotify_id)

df.to_csv("data/pop-punk.csv", index=False)
