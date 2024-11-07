import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# Configure your database URL here
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)

# Function for getting a local session to perform some query/operation on the MYSQL DB, it will be locally injected for the functions in the controller.
# It will also manage closing the database connection for each function.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()