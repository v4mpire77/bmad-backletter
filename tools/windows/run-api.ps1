$env:DATABASE_URL = $env:DATABASE_URL ? $env:DATABASE_URL : "sqlite:///storage/app.db"

python - << 'PY'
from blackletter_api.models.db import Base, get_engine
from blackletter_api.models import tables  # noqa
engine = get_engine()
Base.metadata.create_all(bind=engine)
print("DB ready")
PY

uvicorn apps.api.blackletter_api.main:app --reload --host 127.0.0.1 --port 8000
