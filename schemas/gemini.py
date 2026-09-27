from pydantic import BaseModel
from datetime import datetime

class GeminiPromptResponse(BaseModel):

    positives : str
    negatives : str
    overall   : str 


class GeminiPromptRequest(BaseModel):

    positives : str
    negatives : str
    overall   : str 

