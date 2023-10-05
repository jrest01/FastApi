from fastapi import APIRouter

from fastapi.responses import JSONResponse
from schemas.user import  User
from utils.jwt_manager import create_token

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin123':
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)    