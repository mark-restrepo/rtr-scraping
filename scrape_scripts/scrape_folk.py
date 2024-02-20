import time
from dataclasses import dataclass

import numpy as np
import requests
import tqdm
from bs4 import BeautifulSoup
import pandas as pd

from rtr import Artist
from rtr.geocode import geocode
from rtr.origin import get_origin, get_birthplace
from rtr.spotify import  get_spotify_id

r = requests.get("https://en.wikipedia.org/wiki/List_of_folk_musicians")

soup = BeautifulSoup(r.content, "html.parser")

in_the_us = False

artists = []
for entry in soup.find_all('li'):
    if entry.find("a"):
        if entry.find("a").get('href'):
            if entry.get_text() == "Clarence Ashley":
                in_the_us = True
            if in_the_us:
                a = Artist(entry.get_text())
                a.link = entry.find("a").get('href')
                artists.append(a)
            if entry.get_text() == "Martin Zellar":
                in_the_us = False

for artist in tqdm.tqdm(artists):
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

df["origin_point"] = df["origin"].apply(geocode)
df["birth_point"] = df["birth"].apply(geocode)

df['spotify_id'] = df["name"].apply(get_spotify_id)

df.to_csv("folk.csv", index=False)
