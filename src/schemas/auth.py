import uuid
from typing import Annotated

from pydantic import BaseModel, EmailStr, ConfigDict, Field, BeforeValidator

from .shared import empty_string


class SignUpUsersSchema(BaseModel):
  first_name: Annotated[str, BeforeValidator(empty_string)]
  last_name: Annotated[str, BeforeValidator(empty_string)]
  username: Annotated[str, BeforeValidator(empty_string)]
  email: Annotated[EmailStr, BeforeValidator(empty_string)]
  password: Annotated[str, BeforeValidator(empty_string)]

  model_config = ConfigDict(
    str_strip_whitespace=True,
    extra='ignore',
  )

class SignUpResponseSchema(BaseModel):
  uid: uuid.UUID
  username: str
  email: str
  first_name: str
  last_name: str
  email_verified: bool | None = None










