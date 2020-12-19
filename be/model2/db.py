from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from config import Conf
import psycopg2

class db():
    def __init__(self):
        #engine = create_engine(Conf.get_sql_conf('local_w'))
        #engine = create_engine(Conf.get_sql_conf('local_y'))
        engine = create_engine(Conf.get_sql_conf('local'))
        #engine = create_engine(Conf.get_sql_conf('local'))
        Base = declarative_base()
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()