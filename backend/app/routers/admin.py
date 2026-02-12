from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/pending-sellers", response_model=list[schemas.AdminUserOut])
def pending_sellers(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    return (
        db.query(models.User)
        .filter(models.User.seller_verified == False)  # noqa: E712
        .all()
    )


@router.post("/approve-seller/{user_id}", response_model=schemas.AdminUserOut)
def approve_seller(user_id: int, db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.seller_verified = True
    user.role = models.UserRole.seller.value
    db.commit()
    db.refresh(user)
    return user
