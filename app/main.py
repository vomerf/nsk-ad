from fastapi import FastAPI

from app.api.endpoints.ad import router as ad_router
from app.api.endpoints.comment import router as comment_router
from app.api.endpoints.user import router as user_router
from app.api.endpoints.complaint import router as complaint_router


app = FastAPI()


app.include_router(ad_router)
app.include_router(user_router)
app.include_router(comment_router)
app.include_router(complaint_router)
