from fastapi import APIRouter
from app.core.qkd_engine import run_bb84

router = APIRouter(prefix="/api")


@router.get("/test")
def test_api():
    return {"message": "API is running"}


@router.get("/qkd")
def qkd_simulation():
    return run_bb84(n=50)
