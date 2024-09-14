import pandas as pd
from pandas import DataFrame
from ast import literal_eval
from typing import List
from ..schemas.movie import Movie

def get_data_frame():
    """
    Get dataframe with movies and credits data combined by movie 'id'
    
    Return: Combined Dataframe
    """
    
    credits_df = pd.read_csv('movie_recommender/data/tmdb_5000_credits.csv')
    movies_df = pd.read_csv('movie_recommender/data/tmdb_5000_movies.csv')
    
    credits_df.columns = ['id', 'title_c', 'cast', 'crew']
    
    # Merge credits and movies data on movie 'id'
    movies_df = movies_df.merge(credits_df, on='id')
    
    movies_df['poster_path'] = movies_df['poster_path'].fillna('')
    
    # TODO: Use recommender algo to generate vote average
    movies_df['vote_average'] = movies_df['vote_average'].fillna(0)
    movies_df['release_date'] = movies_df['release_date'].fillna('')
    
    return movies_df
    
def convert_string_to_obj(pd: DataFrame, col: str):
    """
    Convert string to object to use it for training model.
    
    Keyword arguments:
    pd: Pandas dataframe.
    col: Column name.
    Return: Converted dataframe
    """
    
    pd[col] = pd[col].apply(literal_eval)
    
    return pd

def get_movies_from_data_frame(df: DataFrame) -> List[Movie]:
    """
    Get Movies object created from dataframe.
    
    Keyword arguments:
    df -- Dataframe.
    Return: List of Movie objects.
    """
    df = df[['id', 'title', 'genres', 'poster_path', 'vote_average', 'release_date']]
    return df.apply(lambda row: Movie(id=row['id'],
                                      title=row['title'],
                                      genres=row['genres'],
                                      poster_path=row['poster_path'],
                                      vote_average=row['vote_average'],
                                      release_date=row['release_date']),
                    axis=1).tolist()
    