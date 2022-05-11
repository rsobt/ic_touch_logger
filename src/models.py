from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    student_id = Column(String(255), unique=True, nullable=False)
    need_update_log = Column(Boolean, default=False)
    need_notification = Column(Boolean, default=False)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_logs = relationship("Log", backref="user")


class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(255), ForeignKey("user.student_id"), nullable=False)
    action = Column(String(255), nullable=False)
    slack_th = Column(String(255), default=None)
    create_at = Column(DateTime, default=datetime.now)
