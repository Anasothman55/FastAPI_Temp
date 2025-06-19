from typing import Sequence

from src.database.model import UserModel


async def validate_unique(exist_user: Sequence[UserModel], email, username)-> list[dict]:
  errors = []
  for u in exist_user:
    if u.email == email:
      errors.append({
        "loc": 'email',
        "value": email,
        "message": "This email is already registered"
      })
    if u.username == username:
      errors.append({
        "loc": 'username',
        "value": username,
        "message": "This username is already taken"
      })

  return errors





