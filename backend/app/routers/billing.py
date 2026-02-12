from fastapi import APIRouter

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.get("/")
def list_billing():
    return {"billing": []}
