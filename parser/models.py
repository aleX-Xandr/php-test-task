
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    url = Column(String(255), unique=True)
    publication_date = Column(DateTime)
    author = Column(String(255))
    tags = Column(String(255))