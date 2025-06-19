from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_engine import async_session_maker

#? get db dependencies with this code we can access the database
async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as db:
    try:
      yield db
    except Exception as e:
      await db.rollback()
      print(e)
      raise
    finally:
      await db.close()









