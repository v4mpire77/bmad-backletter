import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read DB URL from env; default to local SQLite for dev/test
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_local.db")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Ensure models are imported so metadata is populated in simple setups/tests
try:
    from .models import entities  # noqa: F401
except Exception:
    # In some test contexts, models may be imported later; ignore here
    pass

# Auto-create tables in lightweight SQLite dev/test environments
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # If migrations are used in production, this silent fallback is acceptable for tests
    pass


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
