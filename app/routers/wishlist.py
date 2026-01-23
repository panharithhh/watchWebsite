from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


@router.get("/{userId}", response_model=list[schemas.WishlistItemOut])
def listWishlist(
    userId: int,
    db: Session = Depends(get_db),
):
    return db.query(models.WishlistItem).filter(models.WishlistItem.user_id == userId).all()


@router.post("", response_model=schemas.WishlistItemOut)
def addWishlistItem(
    data: schemas.WishlistItemCreate,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    watch = db.query(models.Watch).filter(models.Watch.id == data.watch_id).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    existing = (
        db.query(models.WishlistItem)
        .filter(
            models.WishlistItem.user_id == data.user_id,
            models.WishlistItem.watch_id == data.watch_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Watch already in wishlist")

    item = models.WishlistItem(user_id=data.user_id, watch_id=data.watch_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{wishlistItemId}")
def removeWishlistItem(
    wishlistItemId: int,
    db: Session = Depends(get_db),
):
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == wishlistItemId).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    db.delete(item)
    db.commit()
    return {"message": "Wishlist item removed"}
