from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "the mini cloud is running"}