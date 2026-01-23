from logging import raiseExceptions
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from pydantic_core.core_schema import model_field
from sqlalchemy.orm import Session
from sqlalchemy import schema, text
from database import SessionLocal, engine, get_db
import models
import schemas

router = APIRouter(
    prefix="/watches",
    tags=["Watches"]
)

@router.post("/getWatch")
def createWatch(data : schemas.WatchCreate, db : Session = Depends(get_db)):
    watch = models.Watch(**data.model_dump()) 
    db.add(watch)
    db.commit()
    db.refresh(watch)
    return watch


@router.post("/{watchID}")
def deleteWatch(watchID : int , db : Session = Depends(get_db)):

    watchDeleted = db.query(models.Watch).filter(models.Watch.id == watchID).first()
    

    if not watchDeleted:
        raise HTTPException(status_code=404, detail ="watch not foudn") 

    db.delete(watchDeleted)
    db.commit()
    
    return {"message" : "Watch is successfully deleted"} 


@router.put("/{watchID}")
def updateWatch(watchID: int, data : schemas.WatchUpdate, db:Session = Depends(get_db)  ):
     
    watch = db.query(models.Watch).filter(models.Watch.id == watchID).first()

    if not watch:
        raise HTTPException(status_code=404, detail ="watch not foudn") 

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(watch, key, value)

    db.commit()
    db.refresh(watch)
    return watch    
        
