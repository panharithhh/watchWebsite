from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import schema, text
from database import SessionLocal, engine, get_db
import models 
import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signUp", response_model=schemas.UserOut)
def sign_up(user_cred: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_cred.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        username=user_cred.username,
        email=user_cred.email,
        password_hash=user_cred.password_hash 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(data: schemas.UserLogin, db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == data.email).first()
    
    if user :
        if (data.password_hash == user.password_hash):
            return {"msg" : "Login successful"}
        else: 
            return {"msg" : " Wrong password, or Wrong Login"} 
    else :
        return {"message" : "This account email doesn't exist"}

        
    
