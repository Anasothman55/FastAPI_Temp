import uvicorn
from src.core.config import setting

if __name__ == '__main__':
  uvicorn.run(
    'src.main:app',
    host=setting.SERVER_DOMAIN,
    port=setting.SERVER_PORT,
    reload=True
  )


