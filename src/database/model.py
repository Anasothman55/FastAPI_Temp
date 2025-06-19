from datetime import datetime, timezone, date, time
import uuid
from typing import Optional

from sqlmodel import SQLModel, Field, Column, TIMESTAMP
import sqlalchemy.dialects.postgresql as pg

def get_timestamp() -> datetime:
  return datetime.now(timezone.utc)
def get_date() -> date:
  return get_timestamp().date()
def get_time()-> time:
  return get_timestamp().time()


var = 'obj'

class UserModel(SQLModel, table=True):
  __tablename__ = 'users'

  uid: uuid.UUID = Field(default_factory= uuid.uuid4, primary_key=True, index=True)
  email: str = Field(nullable=False, unique=True, index=True)
  username: str = Field(nullable=False, unique=True, index=True)
  password_argon: str = Field(nullable=False, exclude=True)
  role: str = Field(default='client', nullable=False)

  first_name: Optional[str]
  last_name: Optional[str]
  phone: Optional[str]
  avatar_url: Optional[str]

  email_verified: bool = Field(default=False)
  email_verification_token: Optional[str] = Field(index=True)
  email_verification_expire_at: Optional[datetime]

  password_reset_token: Optional[str] = Field(index=True)
  password_reset_expires_at: Optional[datetime]

  is_active: bool = Field(default=True)
  is_delete: bool = Field(default=False)
  account_locked: bool = Field(default=False)

  last_login_at: Optional[datetime]
  created_at: datetime = Field(default_factory=get_timestamp,sa_column=Column(TIMESTAMP(timezone=True)))
  updated_at: datetime = Field(default_factory=get_timestamp,sa_column=Column(TIMESTAMP(timezone=True),onupdate=get_timestamp))


"""
-- User roles/permissions
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions/tokens
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address INET
);

-- Social auth providers
CREATE TABLE user_social_accounts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    provider VARCHAR(50) NOT NULL, -- 'google', 'github', etc.
    provider_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""




