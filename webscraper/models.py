from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import yaml


with open("config.yml", "r") as yml:
    cfg = yaml.safe_load(yml)

# Connect to postgres database.
engine = create_engine(cfg["db_connection"]["postgres"])
# Bind session with the enginee. What database should it intereact is defined in bind parameter.
Session = sessionmaker(bind=engine)
# Initialize the session. To query against the db.
session = Session()
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


if __name__ == "__main__":
    # Testing
    gpu1 = GpuAvailability(
        name="name", model="model", sku="sku", available=True, price="12.50"
    )
    session.add(gpu1)
    session.commit()
