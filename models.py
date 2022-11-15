from sqlalchemy import Column, Integer, String, MetaData, Table, ForeignKey
from database import Base

meta = MetaData()
students=Table(
    'students',meta,
    Column('id',Integer,primary_key=True),
    Column('fname',String(255)),
    Column('lname',String(255)),
    Column('phone',String(255)),
    Column('course',String(255)),
    Column('gender',String(255)),
    Column('country',String(255), ForeignKey("country.id")),
    Column('state',String(255), ForeignKey("state.id")),
    Column('city',String(255), ForeignKey("city.id")),
    Column('address',String(255)),
    Column('vehicle', String(225)),
    Column('image', String(225))
)

country = Table(
    'country', meta, 
    Column('id',Integer,primary_key=True),
    Column('name',String(255))
)

state = Table(                               
    'state', meta,                            
    Column('id',Integer,primary_key=True),
    Column('name',String(30)),
    Column('country_id', Integer)
)

city = Table(                               
    'city', meta,                              
    Column('id',Integer,primary_key=True),
    Column('name', String(30)),
    Column('state_id', Integer)
)

