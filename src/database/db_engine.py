
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel,text

from src.core.config import setting






engine = create_async_engine(
  url= setting.POSTGRESQL_URI,
  echo = False,

  pool_size = 10,
  max_overflow= 20,
  pool_timeout= 30,
  pool_recycle= 3600,
)

async_session_maker = sessionmaker(
  bind=engine,
  class_= AsyncSession,
  expire_on_commit=False
)


async def close_db_connection():
  await engine.dispose()

async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)
    print("Database table create successfully")

  async with async_session_maker() as db:
    result = await db.execute(text("SELECT 1"))
    scalar_result = result.scalar_one()
    print(f"Connection test result: {scalar_result}")  # Should print 1

