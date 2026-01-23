from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.post("")
def searchWatch(searchQuery: schemas.WatchSearch, db: Session = Depends(get_db)):
    
    query = db.query(models.Watch)
    
    if searchQuery.name:
        query = query.filter(models.Watch.name.ilike(f"%{searchQuery.name}%"))

    if searchQuery.tags:
        query = query.filter(models.Watch.tags.ilike(f"%{searchQuery.tags}%"))

    if searchQuery.brand:
        query = query.filter(models.Watch.brand.ilike(f"%{searchQuery.brand}%"))

    return query.all()

@router.post("/trackBrand", response_model=schemas.BrandPreferenceOut)
def trackBrandSearch(
    data: schemas.BrandSearchTrack,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    pref = (
        db.query(models.BrandPreference)
        .filter(
            models.BrandPreference.user_id == data.user_id,
            models.BrandPreference.brand == data.brand,
        )
        .first()
    )
    if pref:
        pref.search_count += 1
    else:
        pref = models.BrandPreference(
            user_id=data.user_id,
            brand=data.brand,
            search_count=1,
        )
        db.add(pref)

    db.commit()
    db.refresh(pref)
    return pref


@router.get("/recommended/{userId}")
def recommendedWatches(
    userId: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    topPrefs = (
        db.query(models.BrandPreference)
        .filter(models.BrandPreference.user_id == userId)
        .order_by(desc(models.BrandPreference.search_count))
        .limit(3)
        .all()
    )
    if not topPrefs:
        return []

    brands = [pref.brand for pref in topPrefs]
    watches = (
        db.query(models.Watch)
        .filter(models.Watch.brand.in_(brands))
        .filter(models.Watch.status == models.WatchStatus.approved)
        .all()
    )

    scores = {pref.brand: pref.search_count for pref in topPrefs}
    response = []
    for watch in watches:
        response.append(
            {
                "watch_id": watch.id,
                "score": scores.get(watch.brand, 0),
            }
        )
    return response
