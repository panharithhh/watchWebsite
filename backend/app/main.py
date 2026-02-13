from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

from routers import admin, auth, catalog, emails, search, users, watches, wishlist, promotion, billing, services

app = FastAPI(title="API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=[
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
#     "https://watch123-dusky.vercel.app",
#   ],
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"],
# )

# allow_origins=[
#   "http://localhost:5173",
#   "http://127.0.0.1:5173",
#   "https://watch123-dusky.vercel.app",
#   "https://watch123-55p5suake-chea-panhariths-projects.vercel.app",
# ]

# app.add_middleware(
#   CORSMiddleware,
#   allow_origin_regex=r"^https://.*\.vercel\.app$",
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://watch123-55p5suake-chea-panhariths-projects.vercel.app",
    ],
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



