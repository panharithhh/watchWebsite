from fastapi import FastAPI
from database import Base, engine
from routers import admin, auth, catalog, emails, search, users, watches, wishlist, promotion, billing 
import models 

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(watches.router)
app.include_router(emails.router)
app.include_router(catalog.router)
app.include_router(search.router)
app.include_router(wishlist.router)
app.include_router(admin.router)
app.include_router(billing.router)
app.include_router(promotion.router)
