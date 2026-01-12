from fastapi import FastAPI
from database import Base, engine
from routers import users, watches,emails
import models 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(watches.router)
app.include_router(emails.router)

