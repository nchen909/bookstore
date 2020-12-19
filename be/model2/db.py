from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

import psycopg2

class db():
    def __init__(self):
        #engine = create_engine(Conf.get_sql_conf('local_w'))
        #engine = create_engine(Conf.get_sql_conf('local_y'))
        engine = create_engine('postgresql://postgres:@localhost:5432/bookstore')
        #engine = create_engine(Conf.get_sql_conf('local'))
        Base = declarative_base()
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()