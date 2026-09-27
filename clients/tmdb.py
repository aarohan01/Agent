from dotenv import load_dotenv
import os 
import httpx
import sys
from httpx import AsyncHTTPTransport, HTTPTransport
from schemas.tmdb import TMDBSearchResponse, TMDBReviewResponse, TMDBDetailResponse
from schemas.movies import MovieSearch, MovieReview, MovieDetail
### ENV and Headers ###
load_dotenv()
'''
use environ instead of getenv.
getenv returns None, environ crashes immediatedly
tmdb_token = os.getenv("TMDB_TOKEN")
'''
try:
    tmdb_token = os.environ["TMDB_TOKEN"]
except KeyError as e:
    print(f"Token Error : {e}")
    sys.exit(1)

headers = { "accept": "application/json", "Authorization": f"Bearer {tmdb_token}"}
async_client = httpx.AsyncClient(timeout=10.0, transport=AsyncHTTPTransport(retries=3))
client = httpx.Client(timeout=10.0, transport=HTTPTransport(retries=3))



### API calls ###
''' 
### TEST API ###
def get_movie_details(movie_id: int):

    movie_details = httpx.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}",headers={
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_token}"},
    timeout=10
    )


    print(movie_details.headers['content-type'])
    print(movie_details.status_code)
    print(json.dumps(movie_details.json(), indent=2))

'''

async def get_search_movie(movie_name : str) -> MovieSearch:

    '''
    This function searches the tmdb for the movie name if it matches exact then return the movie id if not return the 
    suggestions.
    '''
    # TODO -> Async 

    movie_found = False
    movie_id = None 
    suggestions = []

    #response = client.get(url=f"https://api.themoviedb.org/3/search/movie",headers=headers, params={"query" : f"{movie_name}"})
    response = await async_client.get(url=f"https://api.themoviedb.org/3/search/movie",headers=headers, params={"query" : f"{movie_name}"})
    response.raise_for_status()  #Httpx doesn't raise error for 4xx and 5xx by default

    ### .json() returns python dict 
    response_model = TMDBSearchResponse.model_validate(response.json())

    # Search the result for exact match, add all not exact to suggestions
    # Case 1 : empty result -> movie not found, no similar suggestions found 
    # Case 2 : movie found exact -> movie found + suggestions
    # Case 3 : movie not found exact -> movie not found + suggestions
    results = response_model.results
    if results:
        movie_name_normalized = movie_name.strip().casefold()
        for r in results:

            if not movie_found and r.title.strip().casefold() ==  movie_name_normalized:
                movie_found = True
                movie_id = r.id
            else:
                suggestions.append(r.title)

    min_suggest = min(len(suggestions),5)
    movie_search =  MovieSearch.model_validate({'movie_found' : movie_found, 'movie_id' : movie_id, 'suggestions' : suggestions[:min_suggest]})
    return movie_search





async def get_movie_reviews(movie_id) -> list[MovieReview]:

    '''
    This function gets the first page of reviews from the tmdb api and returns a list.
    By default the movie id is set to Interstellar, for experimenting.
    '''
    # TODO Convert later to async, if the route in ours is also async
    
    #response = client.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}/reviews",headers=headers)
    response = await async_client.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}/reviews",headers=headers)
    response.raise_for_status()  #Httpx doesn't raise error for 4xx and 5xx by default

    ### .json() converts to python dict, .text will give raw json string ###
    response_model = TMDBReviewResponse.model_validate(response.json())
    reviews = []

    ### Looping python dict for only the keys we need in result ###
    results = response_model.results
    for r in results:

        # Converting to pydantic model TMDBMovieReviews
        review = MovieReview.model_validate({"author" : r.author, "rating" : r.rating, "review" : r.content[:2000]})
        reviews.append(review)

    return reviews



async def get_movie_details(movie_id: int) -> MovieDetail:

    #response = client.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}",headers=headers)
    response = await async_client.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}",headers=headers)
    response.raise_for_status()  #Httpx doesn't raise error for 4xx and 5xx by default

    # Validate external response
    response_model = TMDBDetailResponse.model_validate(response.json())

    # response_model is already pydantic so converting to dict and validating in output model 
    details = MovieDetail.model_validate({"details" : f"{response_model.overview}"})

    return details


if __name__ == "__main__":

    #movie_id = 157336
    #movie_name = "Interstellar"
    #ms = get_search_movie(movie_name)
    #print(get_movie_reviews(ms.movie_id))
    #print(ms.suggestions)
    pass




