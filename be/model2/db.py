from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
import psycopg2

class db():
    def __init__(self):
        engine = create_engine('postgresql://postgres:amyamy@localhost:5433/bookstore')
        #engine = create_engine('postgresql://postgres:990814@[2001:da8:8005:4056:81e9:7f6c:6d05:fe47]:5432/bookstore')

        Base = declarative_base()
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()