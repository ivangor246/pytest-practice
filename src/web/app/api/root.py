from fastapi import APIRouter

from app.api.trading import trading_router

root_router = APIRouter(prefix='/api')

root_router.include_router(trading_router)
