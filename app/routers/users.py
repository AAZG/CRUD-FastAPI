from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.users import User

users_router = APIRouter()


@users_router   .post("/login", tags=['auth'])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == 12345):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={
                                "message": "Get all films successfully",
                                "details": token
                                }
                            )
    else:
        return JSONResponse(status_code=401, 
                            content={"message": "Credenciales inválidas, intente de nuevo"})