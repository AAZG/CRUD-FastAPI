from pydantic import BaseModel

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