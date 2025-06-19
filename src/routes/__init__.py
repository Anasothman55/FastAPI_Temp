from .auth import route as auth_router

from fastapi import APIRouter


root = APIRouter()


root.include_router(router=auth_router,prefix='/auth')






