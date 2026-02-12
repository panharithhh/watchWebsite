from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from database import get_db
from security import get_current_user
import models

router = APIRouter(prefix="/promotion", tags=["Promotion"])

_PROMOTIONS: list[dict] = []
_PROMO_ID = 1


@router.get("/")
def list_promotions():
    return {"promotions": _PROMOTIONS}


@router.post("/", response_model=schemas.PromotionOut)
def create_promotion(
    payload: schemas.PromotionCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role != models.UserRole.seller.value:
        raise HTTPException(status_code=403, detail="Seller access required")

    watch = db.query(models.Watch).filter(models.Watch.id == payload.watch_id).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")
    if watch.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot promote another seller's watch")

    existing = next(
        (
            promo
            for promo in _PROMOTIONS
            if promo.get("watch_id") == payload.watch_id and promo.get("seller_id") == user.id
        ),
        None,
    )

    if existing:
        existing.update(
            {
                "title": payload.title,
                "description": payload.description,
                "discount": payload.discount,
                "valid_until": payload.valid_until,
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        return existing

    global _PROMO_ID
    promo = {
        "id": _PROMO_ID,
        "title": payload.title,
        "description": payload.description,
        "watch_id": payload.watch_id,
        "discount": payload.discount,
        "valid_until": payload.valid_until,
        "seller_id": user.id,
        "created_at": datetime.utcnow().isoformat(),
    }
    _PROMO_ID += 1
    _PROMOTIONS.append(promo)
    return promo
