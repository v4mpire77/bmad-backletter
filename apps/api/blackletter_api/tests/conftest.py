import sys
from pathlib import Path

# Ensure `apps/api` is on sys.path so `import blackletter_api` works
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import create_engine

from blackletter_api import database
from blackletter_api.models import entities

# Rebind engine to a known absolute path and ensure tables exist
db_path = Path(__file__).resolve().parents[3] / "test.db"
database.engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)
database.SessionLocal.configure(bind=database.engine)
entities.Base.metadata.create_all(bind=database.engine)

