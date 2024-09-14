from fastapi import APIRouter, Query, Request
from typing import List
import random
from ..schemas.movie import Movie, MovieRecommendation
from ..recommender.app import get_recommendations
from ..utils.file_utils import append_to_csv_file, read_csv_File
from ..utils.pandas_utils import get_movies_from_data_frame
from ..constants.app_constants import USER_SEARCHED_MOVIES_FILEPATH

router = APIRouter(
    prefix="/api/movies"
)

@router.get("/", response_model=List[Movie])
def get_movies(request: Request) -> List[Movie]:
    """
    Return list of movies.
    
    Keyword arguments:
    request -- Request.
    Return: List of Movie objects.
    """
    return get_movies_from_data_frame(request.app.state.model)

@router.get("/autocomplete", response_model=List[str])
def get_prefix_movies(
    request: Request,
    movie_name: str = Query(..., min_length=1)) -> List[str]:
    """
    Get list of movies that matches the current prefix.
    
    Keyword arguments:
    request -- Request
    movie_name: Prefix of the movie name.
    Return: List of matching movies.
    """
    prefix_tree = request.app.state.prefix_tree
    matched_movie_names: List[str] = prefix_tree.words_with_prefix(movie_name.replace(" ", "").lower())
    
    return matched_movie_names[:min(11, len(matched_movie_names))]

@router.get("/user_liked", response_model=List[Movie])
def get_userliked_movies(request: Request) -> List[Movie]:
    """
    Get the list of liked movies of user.
    
    Keyword arguments:
    request -- Request
    Return: List of Movie objects.
    """
    content = read_csv_File(USER_SEARCHED_MOVIES_FILEPATH)
    if len(content) == 0:
        return []
    
    new_movies = []
    new_movies.append(random.choice(content))
    
    movie_name = new_movies[0][0]
    return get_recommendations(movie_name, request.app.state.model, limit=9)

@router.post("/recommend", response_model=List[Movie])
def recommend_movies(request: Request, movie: MovieRecommendation) -> List[Movie]:
    """
    Use recommendation system to suggest movies to user.
    
    Keyword arguments:
    request -- Request
    movie -- Movie recommendation object
    Return: List of Movie objects.
    """
    movies = get_recommendations(movie.title, request.app.state.model)
    if len(movies) == 0:
        movie_list = get_prefix_movies(request, movie.title) or []

        if len(movie_list) == 0:
            movie_title = get_userliked_movies(request)[0].title
        else:
            movie_title = movie_list[0]

        movie.title = movie_title
        movies = get_recommendations(movie_title, request.app.state.model)

    if len(movies) > 0:
        append_to_csv_file(USER_SEARCHED_MOVIES_FILEPATH, {'Movie':movie.title}, ['Movie'])
    
    return movies
