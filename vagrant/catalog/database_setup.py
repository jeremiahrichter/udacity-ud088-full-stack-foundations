import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

name = ''  # db name goes here

engine = create_engine('sqlite:///{}.db'.format(name))
Base.metadata.create_all(engine)
