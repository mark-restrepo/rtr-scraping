import time

import numpy as np
import requests
import tqdm
from bs4 import BeautifulSoup
import pandas as pd

from rtr import Artist
from rtr.origin import get_origin, get_birthplace


def scrape(url: str, first_musician: str, last_musician: str, genre: str):
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    add_to_list = False

    artists = []
    for entry in soup.find_all('li'):
        if entry.find("a"):
            if entry.find("a").get('href'):
                entry_text = entry.get_text().split('[')[0]
                if entry_text == first_musician:
                    add_to_list = True
                if add_to_list:
                    a = Artist(entry_text)
                    a.link = entry.find("a").get('href')
                    artists.append(a)
                if entry_text == last_musician:
                    add_to_list = False

    for artist in tqdm.tqdm(artists):
        try:
            content = requests.get("https://en.wikipedia.org" + artist.link).content
            artist.origin = get_origin(content)
            artist.birth = get_birthplace(content)
        except Exception:
            artist.origin = None
            artist.birth = None

    df = pd.DataFrame(
        [(a.name, a.link, a.origin, a.birth) for a in artists],
        columns=["name", "link", "origin", "birth"]
    )
    df['birth'] = df.birth.replace({np.nan: None})
    df['origin'] = df.origin.replace({np.nan: None})

    df = df[~df.origin.isnull() | ~df.birth.isnull()]

    df.to_csv(f"data/{genre}.csv", index=False)
