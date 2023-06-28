import uvicorn
from fastapi import FastAPI

from app.api.endpoints.ad import router as ad_router
from app.api.endpoints.comment import router as comment_router
from app.api.endpoints.complaint import router as complaint_router
from app.api.endpoints.user import router as user_router
from app.util.log_file import setup_logging

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    """Действия при запуске сервера."""
    setup_logging()

app.include_router(ad_router)
app.include_router(user_router)
app.include_router(comment_router)
app.include_router(complaint_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)