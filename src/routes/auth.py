from fastapi import APIRouter, Body, Depends, status
from redis.commands.search.query import Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from src.schemas.auth import SignUpUsersSchema, SignUpResponseSchema
from src.services.auth import signup_service, verify_email_service
from src.shared.dependencies import get_db


route = APIRouter(prefix='/v1', tags=['Auth'] )


@route.post('/signup', status_code= status.HTTP_201_CREATED, response_model= SignUpResponseSchema)
async def signup_route(
    schema: Annotated[SignUpUsersSchema , Body()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  res = await signup_service(db, schema)
  return res


@route.post('email-verify', status_code=status.HTTP_200_OK)
async def verify_email(
    token: Annotated[str, Query()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
  await verify_email_service(db,token)


