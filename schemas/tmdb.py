from pydantic import BaseModel, Field, AliasPath

'''
External schemas for validating output of TMDB API
'''
### Model/Schema ###
## Search ##
class TMDBSearchItem(BaseModel):

    id : int 
    title : str 

class TMDBSearchResponse(BaseModel):

    results : list[TMDBSearchItem] 


## Review ##
class TMDBReviewItem(BaseModel):

    content : str
    author : str 
    rating : float | None = Field(validation_alias=AliasPath("author_details", "rating"))


class TMDBReviewResponse(BaseModel):

    results : list[TMDBReviewItem]



## Details ##
class TMDBDetailResponse(BaseModel):

    overview : str



