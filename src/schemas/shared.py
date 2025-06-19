
from typing import AnyStr, Any

from pydantic import BaseModel
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo


def empty_string(v: AnyStr, info: ValidationInfo):
  if v is None or (isinstance(v, str) and v.strip() == ""):
    raise PydanticCustomError(
      "empty_string",
      f"{info.field_name} must not be empty or only whitespace",
      {"field_name": info.field_name}
    )
  return v



class ErrorSchema(BaseModel):
  loc: str
  value: Any
  message: str



