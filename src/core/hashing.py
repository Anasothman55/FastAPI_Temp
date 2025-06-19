
from fastapi import HTTPException, status

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error



ph = PasswordHasher()

def password_hash(password: str) -> str:
  return ph.hash(password)

def password_decode(password_argon: str, password: str) -> bool:
  try:
    res = ph.verify(password_argon, password)
    return res
  except Argon2Error as e :
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
