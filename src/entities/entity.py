from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# postgres database details
db_url = 'localhost:your_db_port'
db_name = 'your_db_name'
db_user = 'your_db_user'
db_password = 'your_db_password'
engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_url}/{db_name}")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():

    # first column in table
    id = Column(Integer, primary_key=True)

    def __init__(self):
        pass

