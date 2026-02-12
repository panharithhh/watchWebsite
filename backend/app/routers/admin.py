from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/pending-sellers", response_model=list[schemas.AdminUserOut])
def pending_sellers(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    users = (
        db.query(models.User)
        .filter(models.User.seller_verified == False)  # noqa: E712
        .all()
    )
    if not users:
        return []
    user_ids = [user.id for user in users]
    docs = (
        db.query(models.SellerDocument)
        .filter(models.SellerDocument.user_id.in_(user_ids))
        .all()
    )
    docs_map: dict[int, list[str]] = {}
    for doc in docs:
        docs_map.setdefault(doc.user_id, []).append(doc.data_url)
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "seller_verified": user.seller_verified,
            "documents": docs_map.get(user.id, []),
        }
        for user in users
    ]


@router.get("/seller-documents", response_model=list[schemas.AdminSellerDocumentsOut])
def seller_documents(db: Session = Depends(get_db), _: models.User = Depends(require_admin)):
    docs = db.query(models.SellerDocument).all()
    if not docs:
        return []
    user_ids = {doc.user_id for doc in docs}
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    user_map = {user.id: user for user in users}
    grouped: dict[int, list[str]] = {}
    for doc in docs:
        grouped.setdefault(doc.user_id, []).append(doc.data_url)
    return [
        {
            "userId": user_id,
            "username": user_map[user_id].username,
            "email": user_map[user_id].email,
            "documents": grouped[user_id],
        }
        for user_id in grouped
        if user_id in user_map
    ]


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
