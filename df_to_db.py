from get_genres import get_genre
from get_artists import get_tracks
import sqlite3
import sqlalchemy
import pandas as pd

def df_to_db():

    df_genre = get_genre()
    df_names = get_tracks()

    df1 = pd.DataFrame(df_genre)
    df2 = pd.DataFrame(df_names)

    merged_df = df1.join(df2, lsuffix="_left").shape 

    return merged_df

    

def create_db():

    table_name = 'Genres'

    df_import = df_to_db()

    df = pd.DataFrame(df_import)

    conn = sqlite3.connect('music_database.db')
    query = f'Create table if not Exists Genres (Genres, Name, Followers, Track, Year)'
    conn.execute(query)
    df.to_sql(table_name,conn,if_exists='replace',index=False)
    conn.commit()
    conn.close()



create_db()