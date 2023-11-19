import enum
import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, types

from chessai import globals as globals_data

if not os.path.exists(globals_data.data_root):
    os.makedirs(globals_data.data_root)
database_path = os.path.abspath(os.path.join(globals_data.data_root, "chessai.db"))
database_url = "sqlite:///{}".format(database_path)
engine = create_engine(database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()


class DateTimeUTC(types.TypeDecorator):
    impl = types.DateTime
    LOCAL_TIMEZONE = datetime.datetime.utcnow().astimezone().tzinfo

    def process_bind_param(self, value: datetime, dialect):
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)
        return value.astimezone(datetime.timezone.utc)

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=datetime.timezone.utc)
        return value.astimezone(datetime.timezone.utc)

class ChessMatch(Base):
    __tablename__ = "chess_match"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTimeUTC, nullable=False, default=datetime.datetime.now)


Base.metadata.create_all(bind=engine)
