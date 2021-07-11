from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


class DBSession:
    def __init__(self, db_uri: str = cfg["db_connection"]["postgres"]):
        # Connect to postgres database.
        engine = create_engine(db_uri)
        # Bind session with the enginee. What database should it intereact is defined in bind parameter.
        Session = sessionmaker(bind=engine)
        # Initialize the session. To query against the db.
        self.session = Session()

    def __enter__(self, db_uri: str = cfg["db_connection"]["postgres"]):
        # Connect to postgres database.
        engine = create_engine(db_uri)
        # Bind session with the enginee. What database should it intereact is defined in bind parameter.
        Session = sessionmaker(bind=engine)
        # Initialize the session. To query against the db.
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def close(self):
        self.session.close()
