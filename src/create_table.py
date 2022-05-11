from sqlalchemy import create_engine

import settings
from models import Base, User, Log

DB_URL = f"mysql://{settings.SQL_USER_NAME}:{settings.SQL_PASSWORD}@localhost/{settings.SQL_DB_NAME}?charset=utf8mb4"
engine = create_engine(DB_URL, echo=True, encoding="utf-8")

Base.metadata.create_all(engine)
