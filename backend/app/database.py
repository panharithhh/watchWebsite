from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#use this when we tryna use docker
# DATABASE_URL = "postgresql://cheapanharith:PASSWORD@db:5432/watch"

#use ths when we run it locally
DATABASE_URL = "postgresql://cheapanharith:PASSWORD@localhost:5432/watch"
    

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
