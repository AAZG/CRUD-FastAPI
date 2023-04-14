from jwt import encode, decode
from dotenv import load_dotenv
import os

def create_token(data: dict) -> str:
    load_dotenv()
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token


def validate_token(token: str) -> dict:
    load_dotenv()
    data: dict = decode(token, 
                        key=os.getenv('SECRET_KEY'), 
                        algorithms=['HS256']
                        )
    return data