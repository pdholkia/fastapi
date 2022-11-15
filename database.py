from sqlalchemy import create_engine, MetaData 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHAMY_DATABASE_URL = 'mysql+pymysql://admin:admin@localhost/office'

engine = create_engine(SQLALCHAMY_DATABASE_URL)

Base = declarative_base()
conn = engine.connect()
print(Base)

Session = sessionmaker(bind = engine)
session = Session()
sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)