from fastapi import APIRouter, Query, Depends
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
import models

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
def list_search_results(
    q: Optional[str] = Query(default=None),
    brand: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Watch)

    if brand:
        brand_term = f"%{brand.strip()}%"
        query = query.filter(models.Watch.brand.ilike(brand_term))
    elif q:
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                models.Watch.name.ilike(term),
                models.Watch.brand.ilike(term),
                models.Watch.tags.ilike(term),
            )
        )

    watches = query.all()
    seller_ids = {watch.seller_id for watch in watches}
    seller_map = {}
    if seller_ids:
        sellers = db.query(models.User).filter(models.User.id.in_(seller_ids)).all()
        seller_map = {seller.id: seller.username for seller in sellers}
    results = [
        {
            "id": watch.id,
            "name": watch.name,
            "brand": watch.brand,
            "price": float(watch.price),
            "description": watch.description,
            "tags": watch.tags,
            "image_url": watch.image_url,
            "status": watch.status,
            "seller_id": watch.seller_id,
            "seller_name": seller_map.get(watch.seller_id),
            "approved_by": watch.approved_by,
        }
        for watch in watches
    ]

    return {"results": results}
