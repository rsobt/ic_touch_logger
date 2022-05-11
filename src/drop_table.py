from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import settings
from models import Base, User, Log

DB_URL = f"mysql://{settings.SQL_USER_NAME}:{settings.SQL_PASSWORD}@localhost/{settings.SQL_DB_NAME}"
engine = create_engine(DB_URL, echo=True)

Log.__table__.drop(engine)
User.__table__.drop(engine)
