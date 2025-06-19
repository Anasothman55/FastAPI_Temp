from datetime import timedelta, datetime, timezone

from fastapi import HTTPException, status
from itsdangerous import  URLSafeTimedSerializer, SignatureExpired, BadSignature
from jose import jwt,JWTError,ExpiredSignatureError

from src.core.config import setting
from src.schemas.shared import ErrorSchema


def jwt_encode(payload: dict, exp_delta: timedelta, key: str) -> str:
  current_time = datetime.now(timezone.utc)
  exp = current_time + exp_delta
  payload['exp'] = exp
  encode_token = jwt.encode(payload, key, algorithm='')
  return encode_token

def jwt_decode(token: str, key: str, options: dict | None = None) -> dict:
  try:
    op = options if options else {}
    payload = jwt.decode(token, key, algorithms='', options=op)
    return payload
  except (ExpiredSignatureError, JWTError) as e:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))






#? email verification token

serializer = URLSafeTimedSerializer(
  secret_key= setting.EMAIL_VERIFY_SECRET,
  salt=setting.EMAIL_VERIFY_SALT
)

def itsdangerous_encode(payload: dict):
  return serializer.dumps(payload)

def itsdangerous_decode(token: str, max_age: int = (3600 * 24 * 2)):
  try:
    return serializer.loads(token, max_age)
  except BadSignature as e:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail={
        'errors':[ErrorSchema(
          loc="token params",
          value=token,
          message=str(e)
        ).model_dump()]
      }
    )
  except SignatureExpired as e:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail={
        'errors':[ErrorSchema(
          loc="token params",
          value=token,
          message=str(e)
        ).model_dump()]
      }
    )

