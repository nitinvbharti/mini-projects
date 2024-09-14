from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from movie_recommender.recommender.app import preprocess_data, get_recommendations
from movie_recommender.data_structures.trie import Trie
from movie_recommender.api import movie
from contextlib import asynccontextmanager
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    model = preprocess_data()
    trie = Trie()
    titles: List[str] = model['title'].tolist()
    
    for title in titles:
        clean_title = title.replace(" ", "").lower()
        trie.insert(clean_title, title)
        
    app.state.model = model
    app.state.prefix_tree = trie
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movie.router)

def main():
    """
    Entry point for app.
    """
    uvicorn.run("movie_recommender.main:app", host="0.0.0.0", port=8001, reload=True)
    
def try_output():
    """
    Test output.
    """
    
    df = preprocess_data()
    movies = get_recommendations('The Hobbit: The Battle of the Five Armies', df)
    
    print(movies)
    
if __name__ == '__main__':
    main()
    