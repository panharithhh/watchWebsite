from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine
import models
import schemas

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS watch"))
    conn.commit()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health_check():
    return {"status": "online"}

@app.post("/signUp", response_model=schemas.UserOut)
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

@app.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or user.password_hash != password:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    return {"message": "Login successful", "user_id": user.id, "role": user.role}

@app.post("/watches", response_model=schemas.WatchOut)
def create_watch(watch: schemas.WatchCreate, db: Session = Depends(get_db)):
    new_watch = models.Watch(**watch.model_dump())
    
    db.add(new_watch)
    db.commit()
    db.refresh(new_watch)
    
    return new_watch

@app.get("/watches", response_model=list[schemas.WatchOut])
def get_all_watches(db: Session = Depends(get_db)):
    return db.query(models.Watch).all()

@app.get("/watches/{watch_id}", response_model=schemas.WatchOut)
def get_watch(watch_id: int, db: Session = Depends(get_db)):
    watch = db.query(models.Watch).filter(models.Watch.id == watch_id).first()
    
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")
        
    return watch

@app.delete("/watches/{watch_id}")
def delete_watch(watch_id: int, db: Session = Depends(get_db)):
    watch = db.query(models.Watch).filter(models.Watch.id == watch_id).first()
    
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")
    
    db.delete(watch)
    db.commit()
    
    return {"message": "Watch deleted successfully"}

@app.put("/watches/{watch_id}", response_model=schemas.WatchOut)
def update_watch(watch_id: int, watch_update: schemas.WatchBase, db: Session = Depends(get_db)):
    watch = db.query(models.Watch).filter(models.Watch.id == watch_id).first()
    
    if not watch:
        raise HTTPException(status_code=404, detail="Watch not found")

    watch.name = watch_update.name
    watch.price = watch_update.price
    watch.brand = watch_update.brand
    watch.description = watch_update.description
    watch.image_url = watch_update.image_url
    watch.tags = watch_update.tags

    db.commit()
    db.refresh(watch)
    
    return watch
