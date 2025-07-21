from fastapi import FastAPI

from app.api.root import root_router
from app.core.config import config

app = FastAPI(
    title=config.TITLE,
    docs_url=config.DOCS_URL,
    openapi_url=config.OPENAPI_URL,
)

app.include_router(root_router)
