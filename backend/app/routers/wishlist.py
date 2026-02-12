from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import get_current_user

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/", response_model=schemas.WishlistResponse)
def list_wishlist(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    items = db.query(models.WishlistItem).filter(models.WishlistItem.user_id == user.id).all()
    watch_ids = [item.watch_id for item in items]
    if not watch_ids:
        return {"wishlist": []}
    watches = db.query(models.Watch).filter(models.Watch.id.in_(watch_ids)).all()
    seller_ids = {watch.seller_id for watch in watches}
    seller_map = {}
    if seller_ids:
        sellers = db.query(models.User).filter(models.User.id.in_(seller_ids)).all()
        seller_map = {seller.id: seller.username for seller in sellers}
    wishlist = []
    for watch in watches:
        data = schemas.WatchOut.model_validate(watch).model_dump(by_alias=True)
        data["sellerName"] = seller_map.get(watch.seller_id)
        wishlist.append(data)
    return {"wishlist": wishlist}


@router.post("/{watch_id}", response_model=schemas.WatchOut)
def add_to_wishlist(
    watch_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    watch = db.query(models.Watch).filter(models.Watch.id == watch_id).first()
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    existing = (
        db.query(models.WishlistItem)
        .filter(models.WishlistItem.user_id == user.id, models.WishlistItem.watch_id == watch_id)
        .first()
    )
    if not existing:
        db.add(models.WishlistItem(user_id=user.id, watch_id=watch_id))
        db.commit()

    return watch


@router.delete("/{watch_id}")
def remove_from_wishlist(
    watch_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    existing = (
        db.query(models.WishlistItem)
        .filter(models.WishlistItem.user_id == user.id, models.WishlistItem.watch_id == watch_id)
        .first()
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    db.delete(existing)
    db.commit()
    return {"ok": True}
