from pydantic import BaseModel, Field

'''
Internal Schemas of the application
'''
### Movie Search Schemas (Non ORM) ###
class MovieSearch(BaseModel):

    movie_found : bool = Field(default=False)
    movie_id : int | None = Field(default=None)
    suggestions : list[str] = Field(default_factory=list)


### Movie Review Schemas (Non ORM) ###
class MovieReview(BaseModel):

    author : str = Field(min_length=1)
    rating : float | None = Field(ge=0, le=10, default=None)
    review : str = Field(min_length=1)   

### Movie Summary Schema (Non ORM) ###
class MovieReviewSummary(BaseModel):

    positives : str 
    negatives : str
    overall   : str 

### Movie Detail Schema (Non ORM) ###
class MovieDetail(BaseModel):

    details : str

### Movie Schema (Non ORM) ###
class MovieDetailsResponse(BaseModel):

    movie_found : bool = Field(default=False)
    movie_id : int | None = Field(default=None)
    suggestions : list[str] = Field(default_factory=list)
    details : str | None = Field(default=None)
    reviews_found : bool = Field(default=False)
    positives : str | None = Field(default=None)
    negatives : str | None = Field(default=None)
    overall   : str | None = Field(default=None)