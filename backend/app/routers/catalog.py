from fastapi import APIRouter

router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/")
def list_catalog():
    return {"catalog": []}
