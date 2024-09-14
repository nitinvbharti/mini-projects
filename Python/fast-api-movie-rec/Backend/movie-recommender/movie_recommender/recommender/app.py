import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..utils.pandas_utils import convert_string_to_obj, get_data_frame, get_movies_from_data_frame
from ..schemas.movie import Movie

def get_director(x):
    """
    Get the director's name from the crew feature.
    If director is not listed, return NaN.
    
    Keyword arguments:
    x -- Dataframe
    Return: Name of director
    """
    for i in x:
        if i['job'] == 'Director':
            return i['name']
        
    return np.nan

def get_list(x):
    """
    Returns the list of top 3 elements or entire list; whichever is more.
    
    Keyword arguments:
    x -- List
    Return: List of top 3 elements.
    """
    if isinstance(x, list):
        names = [i['name'] for i in x]
        
        # Return first 3 names.
        return names[:min(3, len(names))]
    
    # Return empty list in case of invalid/missing data.
    return []

def clean_data(x):
    """
    Removes spaces from strings and converts them to lowercase
    
    Keyword arguments:
    x -- List/String
    Return: Cleaned data.
    """
    if isinstance(x, List):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def create_soup(x):
    """
    Create metadata soup to feed vectorizer.
    
    Keyword arguments:
    x -- DataFrame
    Return: Metadata soup.
    """
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genre_names'])

def preprocess_data():
    """
    Preprocess the data frame, cleans off and returns modified dataframe.
    
    Return: Preporcessed data.
    """
    # Read data from csv files.
    df = get_data_frame()
    
    # The data that needs to be stringified for training model.
    features = ['cast', 'crew', 'keywords', 'genres']
    
    # Parse data to convert to stringified objects.
    for f in features:
        df = convert_string_to_obj(df, f)
        
    # Convert director keys to names in dataframe.
    df['director'] = df['crew'].apply(get_director)
    
    # Get top 3 casts and keywords only.
    for f in ['cast', 'keywords']:
        df[f] = df[f].apply(get_list)
        
    # Get top 3 genres.
    df['genre_names'] = df['genres'].apply(get_list)
    
    # Perform cleanup of data.
    features = ['cast', 'keywords', 'director', 'genre_names']
    
    for f in features:
        df[f] = df[f].apply(clean_data)
    
    df['clean_title'] = df['title'].apply(clean_data)
    
    # Create metadata soup.
    df['soup'] = df.apply(create_soup, axis=1)
    
    return df

def get_recommendations(
    title: str,
    df: DataFrame,
    limit: int = 11) -> List[Movie]:
    """
    Get recommendations for movies.
    
    Keyword arguments:
    title -- Movie title
    df    -- DataFrame
    limit -- Number of movies to recommend
    Return: List of movies.
    """
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    
    # Construct reverse map of indices and movie titles.
    indices = pd.Series(df.index, index=df['clean_title']).drop_duplicates()
    
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    # Get the index of the movie that matches the title.
    clean_title = str.lower(title.replace(' ', ''))
    
    # Return empty if no data in dataset.
    if clean_title not in indices:
        return []
    
    idx = indices[clean_title]
    
    # Get pairwise similarity scores for all movies with current movie.
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the movies based on similarity scores.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse= True)
    
    # Get the scores of the top 'limit' movies.
    sim_scores = sim_scores[1:limit]
    
    # Get the movie indices.
    movie_indices = [i[0] for i in sim_scores]
    
    # Get the movies in selected similarity scores.
    movies = df.iloc[movie_indices]
    
    return get_movies_from_data_frame(movies)
    