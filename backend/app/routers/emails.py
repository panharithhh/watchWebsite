from fastapi import APIRouter

router = APIRouter(prefix="/emails", tags=["Emails"])


@router.get("/")
def list_emails():
    return {"emails": []}
