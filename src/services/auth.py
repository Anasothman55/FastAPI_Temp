from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from rich import print
from fastapi.responses import JSONResponse

from src.database.model import UserModel
from src.mails.generate import generate_new_account_email
from src.schemas.auth import SignUpUsersSchema
from src.core.hashing import password_hash, password_decode
from src.utils.auth import validate_unique
from .user import create_users, update_users, get_user_by_token, get_user_by_uid
from ..core.config import setting
from ..core.security import itsdangerous_decode, itsdangerous_encode
from ..error.user import UserUniqueExceptions
from ..schemas.shared import ErrorSchema


async def signup_service(db: AsyncSession, schema: SignUpUsersSchema) :
  try:
    hashing = password_hash(schema.password)
    user = schema.model_dump(exclude={'password'})
    user['password_argon'] = hashing

    res = await create_users(db, user)
    verify_token = itsdangerous_encode({'uid': str(res.uid)})

    up = {
      "email_verification_token": verify_token,
      "email_verification_expire_at": setting.EMAIL_RESET_TOKEN_EXPIRE_HOURS
    }
    await update_users(db,up, res)
    await generate_new_account_email(res.email, res.username, verify_token)

    return res
  except UserUniqueExceptions as e:
    raise e
  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail={
        "errors" : ["Internal server error"]
      }
    )



async def verify_email_service(db: AsyncSession, token: str) :
  try:
    decode = itsdangerous_decode(token, setting.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    user_by_uid = await get_user_by_uid(decode['uid'],db)
    if user_by_uid.email_verified:
      return JSONResponse(
        content="Your email already verify",
        status_code= status.HTTP_200_OK
      )

    user = await get_user_by_token(token, db)

    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
          "errors": [
            ErrorSchema(loc="token query params", value=token,
              message="No user found"
            ).model_dump()
          ]
        }
      )
    up = {
      "email_verified": True,
      "email_verification_token": None,
      "email_verification_expire_at": None
    }
    await update_users(db,up, user)

    return "email verify successfully"

  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail={
        "errors" : "Internal server error"
      }
    )

