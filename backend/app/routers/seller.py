from fastapi import APIRouter

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.get("/")
def list_sellers():
    return {"sellers": []}
