import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base() #base class for a python obj for table in database

class Career(Base):
	__tablename__ = 'career'

	id = Column(Integer, primary_key = True)
	name = Column(String(100), nullable = False)
	description = Column(String(250))

class Project(Base):
	__tablename__ = 'project'

	title = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)
	description = Column(String(800))
	career_id = Column(Integer, ForeignKey('career.id'))
	career = relationship(Career)

engine = create_engine('sqlite:///exduu.db') #database type and name
Base.metadata.create_all(engine)

