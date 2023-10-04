from pydantic import BaseModel, Field
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from typing import Optional
from starlette.requests import Request

from jwt_manager import validate_token

class Movie(BaseModel):
    id : Optional[int] = None 
    title : str = Field(default = '0000',max_length=20)
    overview : str = Field(min_length=10, max_length=100)
    year : int = Field( le=2024, gt=1920)
    rating : float = Field(ge=1, le=10)
    category : str = Field(min_length=5, max_length=20)
    
    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 999,
                    "title": "Your movie",
                    "overview": "Summary - Summary",
                    "year": 2023,
                    "rating": 5.0,
                    "category": "Fiction"
                }
            ]
        }
    }

    def to_dict(self):
        dict = {
        'id': self.id,
        'title': self.title,
        'overview': self.overview,
        'year': self.year,
        'rating': self.rating,
        'category': self.category
        }
        print(dict)
        return dict
    

class User(BaseModel):
    email: str
    password: str


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid Credentials')