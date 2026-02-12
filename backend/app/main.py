import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

from routers import admin, auth, catalog, emails, search, users, watches, wishlist, promotion, billing, services

app = FastAPI(title="API")

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(services.router)

@app.get("/health")
def health():
    return {"ok": True}
