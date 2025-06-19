from pydantic import BaseModel, Field

import enum

class SortOrder(enum.StrEnum):
  DESC = 'desc'
  ASC = 'asc'

class SortBy(enum.StrEnum):
  Email= 'email'
  USERNAME= 'username'
  ROLE= 'role'
  FIRST_NAME= 'first_name'
  LAST_NAME= 'first_name'
  PHONE= 'phone'
  IS_ACTIVE= 'is_active'
  IS_DELETE= 'is_delete'
  LAST_LOGIN_AT= 'last_login_at'
  CREATED_AT= 'created_at'
  UPDATED_AT= 'updated_at'

class UserFilterQuery(BaseModel):
  page: int | None = 1
  limit: int | None = 10
  sortBy: SortBy | None = SortBy.CREATED_AT
  sortOrder: SortOrder | None = SortOrder.ASC



