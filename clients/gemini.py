from google import genai
from dotenv import load_dotenv
import os
import sys 
from schemas.movies import MovieReview, MovieReviewSummary
from schemas.gemini import GeminiPromptResponse, GeminiPromptRequest


### ENV and Header/Session ###
load_dotenv()
try :
    gemini_api_key = os.environ["GEMINI_API_KEY"]
except KeyError as e:
    print(f"Gemini key not found : {e}")
    sys.exit(1)

# SDK already has retries and timeouts
client = genai.Client(api_key=gemini_api_key)


### API Calls ###
async def get_movie_review_summary(reviews : list[MovieReview]) -> MovieReviewSummary:

    '''
    Get movie review summary based on the reviews fetched by tmdb client
    '''
    # TODO -> streaming

    movie_reviews = ''.join([ f"Review {i} : {r.review}\n\n" for i,r in enumerate(reviews)])
    

    
    prompt = f"""
    Summarize the overall audience opinion from these movie reviews.
    Mention the main positives, main criticisms, and overall sentiment, with no acknowledgement of the prompt.
    Use only the provided reviews. Do not add outside knowledge.
    Reviews: \n\n{movie_reviews}
    """
    #interactions  = await client.interactions.create(
    # Async :
    interactions  = await client.aio.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": GeminiPromptRequest.model_json_schema(), #Provide response schema in json str format to gemini
        }

    )

    # Convert to python dict
    # Can also directly use output_text instead of converting to dict
    # interaction is Gemini SDK and we can convert it to str json, output_text in that is also json str
    gemini_response = GeminiPromptResponse.model_validate_json(interactions.output_text)

    ### gemini_response is pydanctic, so convert to dict ###
    summary = MovieReviewSummary.model_validate(gemini_response.model_dump())
    
    return summary
    


if __name__ == "__main__":
    #res =  get_movie_reviews(157336)
    #print(get_movie_review_summary(res))
    pass