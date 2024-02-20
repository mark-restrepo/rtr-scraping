import psycopg2
import os
import pandas as pd
import numpy as np

df = pd.read_csv("data/soul.csv")

df['birth'] = df.birth.replace({np.nan: None})
df['origin'] = df.origin.replace({np.nan: None})

df['birth_point'] = df.birth_point.replace({np.nan: None})
df['origin_point'] = df.origin_point.replace({np.nan: None})

df = df[["name", "link", "origin", "origin_point", "birth", "birth_point", "spotify_id", "genre"]]

with psycopg2.connect(
        dbname="postgis",
        user="postgres",
        password=os.environ['PSQL_PW']
) as connection:
    with connection.cursor() as cur:
        res = cur.executemany(
            f"INSERT INTO artists "
            f"(name, link, origin, origin_point, birth, birth_point, spotify_id, genre) "
            f"VALUES (%s, %s, %s, st_transform(st_GeomFromText(%s,4326),5070), %s, "
            f"st_transform(st_GeomFromText(%s,4326),5070), %s, %s)",
            df.values
        )
