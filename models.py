from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    experience = Column(Integer)
    education = Column(String)
    skills = Column(Text)  # comma-separated


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    skills = Column(Text)        # comma-separated
    education = Column(String)   # BS / MS
    experience = Column(Integer)
    description = Column(Text)
    salary = Column(Integer, nullable=False)