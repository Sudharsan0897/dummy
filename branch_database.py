# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user_branch_user:WZ1TwBgdPzPhOLpAgZTfNkwe7X2Frj0B@dpg-d553v0m3jp1c739juavg-a.virginia-postgres.render.com/user_branch"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
