from fastapi import HTTPException, status


class UserExceptions(HTTPException):
  pass

class UserUniqueExceptions(UserExceptions):
  def __init__(self, errors):
    super().__init__(
      status_code=status.HTTP_409_CONFLICT,
      detail= {
        "errors": errors
      }
    )