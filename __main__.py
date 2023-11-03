import pandas as pd

from get_genres import get_genre
from get_artists import get_tracks


def df_to_db():
    '''Retrieve Spotify data
       Turn into dataframes
       Load data into csv files
    '''
    df_genre = get_genre()
    df_names = get_tracks()

    df1 = pd.DataFrame(df_genre)
    df2 = pd.DataFrame(df_names)

    # Add your own directory path
    df1.to_csv('./data-pipeline/genre_database.csv')
    df2.to_csv('./data-pipeline/artist_database.csv')

 
if __name__ == "__main__":
    df_to_db()