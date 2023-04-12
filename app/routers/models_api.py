from pydantic import BaseModel, Field, validator
from typing import Optional, Union
import datetime
from fastapi.security import HTTPBearer
from fastapi import Request
from routers.jwt_manager import validate_token
from fastapi import HTTPException

class MovieAPI(BaseModel):
    # id: Union[int, None] = Field(None, ge=1, le=2000)
    # # Optional[int] = None
    
                    
    title: str = Field(min_length=5, max_length=20,
                       title="Movie title",
                       description="This is the movie title"
                       )
    
    overview: str = Field(min_length=10, max_length=200,
                          title="Movie Overview",
                          description="This is the movie overview"
                          )
    
    year: int = Field(ge=1900, le=datetime.date.today().year,
                      title="Movie year",
                      description="This is the movie year"
                      )
    
    rating: Union[float, int] = Field(ge=0, le=10,
                                      title="Movie rating",
                                      description="This is the movie rating"
                                      )
    
    category: str = Field(min_length=5, 
                         max_length=20,
                         title="Movie category",
                         description="This is the movie category"
                         )
        
    @validator('rating', pre=True)
    def validate_rating(cls, v):
        if isinstance(v, int):
            return float(v)
        return round(float(v), 1)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "The Godfather",
                "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "year": 1972,
                "rating": 9.2,
                "category": "Crime"
            }
        }
        # exclude = ['id']
        
        
class User(BaseModel):
    email: str
    password: int
    
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": 12345,
            }
        }
        
        
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")