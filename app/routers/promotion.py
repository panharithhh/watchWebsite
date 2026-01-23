from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)


def getSellerUser(sellerId: int, db: Session) -> models.User:
    sellerUser = db.query(models.User).filter(models.User.id == sellerId).first()
    if not sellerUser or sellerUser.role != models.UserRole.seller:
        raise HTTPException(status_code=403, detail="Seller privileges required")
    return sellerUser


@router.post("", response_model=schemas.PromotionOut)
def createPromotion(
    sellerId: int,
    data: schemas.PromotionCreate,
    db: Session = Depends(get_db),
):
    getSellerUser(sellerId, db)
    if data.discount_percent < 1 or data.discount_percent > 100:
        raise HTTPException(status_code=400, detail="discount percent must be between 1 and 100")

    watch = db.query(models.Watch).filter(models.Watch.id == data.watch_id).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    promotion = models.Promotion(
        title=data.title,
        discount_percent=data.discount_percent,
        start_date=data.start_date,
        end_date=data.end_date,
        watch_id=data.watch_id,
    )
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


@router.delete("/{promotionId}")
def deletePromotion(
    promotionId: int,
    sellerId: int,
    db: Session = Depends(get_db),
):
    getSellerUser(sellerId, db)
    promotion = db.query(models.Promotion).filter(models.Promotion.id == promotionId).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")

    db.delete(promotion)
    db.commit()
    return {"message": "Promotion deleted"}


