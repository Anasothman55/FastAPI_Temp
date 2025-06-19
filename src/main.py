from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.db_engine import init_db, close_db_connection
from src.routes import root

@asynccontextmanager
async def life_span(app: FastAPI):
  try:
    await init_db()
  except Exception as e:
    print(f"Error during startup: {str(e)}")
    raise
  yield
  try:
    await close_db_connection()
  except Exception as e:
    print(f"Error closing database connection: {str(e)}")

app = FastAPI(
  title="Base Template Fastapi",
  version="0.1.0",
  lifespan= life_span,
  contact= {
    "email": "anasothman581@gmail.com"
  }
)


app.include_router(router= root)



