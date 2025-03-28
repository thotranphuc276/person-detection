from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from app.config import settings

def get_db_engine(max_retries=5, retry_delay=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                pool_timeout=30,
                pool_recycle=1800,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "person_detection"
                }
            )
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return engine
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(retry_delay)
            continue
        except Exception as e:
            raise e

engine = get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()