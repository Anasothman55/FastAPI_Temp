import uuid
from dataclasses import dataclass
from typing import Any, Type, Sequence

from certifi import where
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlmodel import select, SQLModel, desc,asc,or_, and_

from src.database.model import UserModel
from src.error.user import UserUniqueExceptions
from src.schemas.shared import ErrorSchema
from src.schemas.users import UserFilterQuery


async def _statement(db:AsyncSession,field: str, value: Any)-> AsyncResult:
  statement = select(UserModel).where(getattr(UserModel, field) == value)
  return await db.execute(statement)

async def get_user_by_email(email: EmailStr,db:AsyncSession):
  query = await _statement(db, 'email', email)
  return query.scalar_one_or_none()

async def get_user_by_username(username: str,db:AsyncSession):
  query = await _statement(db, 'username', username)
  return query.scalar_one_or_none()

async def get_user_by_uid(uid: uuid.UUID, db:AsyncSession)-> UserModel:
  query = await _statement(db, 'uid', uid)
  return query.scalar_one_or_none()

async def get_user_by_token(token: str, db:AsyncSession) -> UserModel:
  query = await _statement(db, 'email_verification_token', token)
  return query.scalar_one_or_none()




async def create_users(db: AsyncSession, data: dict)-> UserModel:
  ex = await is_unique(db, data['email'], data['username'])
  if ex: raise UserUniqueExceptions(ex)

  new_user = UserModel(**data)
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

async def is_unique(
    db: AsyncSession,
    email: str,
    username: str
  ):

  filters = [UserModel.email == email, UserModel.username == username]

  statement = select(UserModel).where(or_(*filters))
  res = await db.execute(statement)
  users =  res.scalars().all()

  errors = []

  for u in users:
    if u.email == email:
      errors.append(ErrorSchema(loc='email',value=email,
        message="This email is already registered"
      ).model_dump())
    if u.username == username:
      errors.append(ErrorSchema(loc='username',value=username,
        message="This username is already taken"
      ).model_dump())

  return errors



async def get_all_users(db: AsyncSession, filters: UserFilterQuery):
  sort = getattr(UserModel, filters.sortBy)
  sort = asc(sort) if filters.sortOrder == 'asc' else desc(sort)

  query = select(UserModel).order_by(sort)
  res = await db.execute(query)
  return res.scalars().all()

async def update_users(db: AsyncSession, new_data: dict, row: UserModel):
  for k,v in new_data.items():
    setattr(row, k, v)
  await db.commit()
  await db.refresh(row)
  return row

async def delete_user(db: AsyncSession, row):
  await db.delete(row)
  await db.commit()


async def unique_check(db: AsyncSession, email, username):
  statement = select(UserModel).where(
    or_(
      UserModel.email == email,
      UserModel.username == username
    )
  )
  res = await db.execute(statement)
  return res.scalars().all()
