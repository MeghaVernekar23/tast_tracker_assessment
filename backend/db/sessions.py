from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models.db_models import Base

DATABASE_URL = "sqlite:///./tasktracker.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.rollback()
        raise
    finally:
        db.close()    