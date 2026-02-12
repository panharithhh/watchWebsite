from logging import raiseExceptions
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from pydantic_core.core_schema import model_field
from sqlalchemy.orm import Session
from sqlalchemy import schema, text
from database import SessionLocal, engine, get_db
import models
from security import get_current_user
import schemas

router = APIRouter(
    prefix="/watches",
    tags=["Watches"]
)


@router.get("/mine", response_model=list[schemas.WatchOut])
def list_my_watches(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if user.role not in [models.UserRole.seller.value, models.UserRole.admin.value]:
        raise HTTPException(status_code=403, detail="Seller access required")
    if user.role == models.UserRole.admin.value:
        return db.query(models.Watch).all()
    return db.query(models.Watch).filter(models.Watch.seller_id == user.id).all()


@router.post("/getWatch", response_model=schemas.WatchOut)
def createWatch(
    data: schemas.WatchCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if user.role != models.UserRole.seller.value:
        raise HTTPException(status_code=403, detail="Seller access required")

    payload = data.model_dump(by_alias=False)
    payload["seller_id"] = user.id
    payload["status"] = "approved"
    payload["approved_by"] = user.id
    watch = models.Watch(**payload)
    db.add(watch)
    db.commit()
    db.refresh(watch)
    return watch


@router.post("/{watchID}")
def deleteWatch(
    watchID: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):

    watchDeleted = db.query(models.Watch).filter(models.Watch.id == watchID).first()
    

    if not watchDeleted:
        raise HTTPException(status_code=404, detail ="watch not foudn") 

    if user.role != models.UserRole.admin.value and watchDeleted.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(watchDeleted)
    db.commit()
    
    return {"message" : "Watch is successfully deleted"} 


@router.put("/{watchID}", response_model=schemas.WatchOut)
def updateWatch(
    watchID: int,
    data : schemas.WatchUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
     
    watch = db.query(models.Watch).filter(models.Watch.id == watchID).first()

    if not watch:
        raise HTTPException(status_code=404, detail ="watch not foudn") 

    if user.role != models.UserRole.admin.value and watch.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for key, value in data.model_dump(exclude_unset=True, by_alias=False).items():
        setattr(watch, key, value)

    db.commit()
    db.refresh(watch)
    return watch    
        
