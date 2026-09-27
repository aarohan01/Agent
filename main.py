from fastapi import FastAPI, status, HTTPException
from clients import tmdb, gemini
from schemas.movies import MovieDetailsResponse
from fastapi.middleware.cors import CORSMiddleware
import os

### APP ###
app = FastAPI()

### CORS ###
origins = os.environ["CORS_ORIGINS"].split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/movie", status_code=status.HTTP_200_OK)
#def get_movie_details(movie_name : str) :
async def get_movie_details(movie_name : str) :

    # TODO -> Async 
    
    
    # Already validated search result
    ## Final Model with some default values 
    movie_response = MovieDetailsResponse()

    # Search , update the resoponse especially for suggestions
    search_result = await tmdb.get_search_movie(movie_name=movie_name)
    movie_response = movie_response.model_copy(update=search_result.model_dump())

    # If not available update response and return 
    if not search_result.movie_found:
        return movie_response

    # If movie search exists then update details
    movie_details = await tmdb.get_movie_details(search_result.movie_id)
    movie_response = movie_response.model_copy(update=movie_details.model_dump())


    # If movie search exists then update then  check reviews
    movie_reviews = await tmdb.get_movie_reviews(search_result.movie_id)
    # If no reviews return 
    if not movie_reviews:
        return movie_response

    movie_response = movie_response.model_copy(update={"reviews_found": True})
    #print(movie_response.model_dump())
    # If reviews found get the summary and update both the status and the content
    movie_review_summary = await gemini.get_movie_review_summary(movie_reviews)
    movie_response = movie_response.model_copy(update=movie_review_summary.model_dump())

    return movie_response



