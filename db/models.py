from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey

"""
`declarative_base` is factory function that constructs a base class for declarative class definitions.
SQL alchemy should know about the models we've defined. So we let it no by extending from Base.
"""
Base = declarative_base()


class GpuAvailability(Base):
    __tablename__ = "gpu_availability"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    model = Column(String(128))
    sku = Column(String(128))
    available = Column(Boolean)
    price = Column(Numeric(precision=12, scale=2))
    update_time = Column(DateTime, default=datetime.now())


class Subscribers(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128))


class Urls(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    short_name = Column(String(128))
    comment = Column(String(256))


class SubscribersToUrl(Base):
    __tablename__ = "subscribers_to_url"
    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"))
    url_id = Column(Integer, ForeignKey("urls.id"))
    pattern = Column(String(128))
