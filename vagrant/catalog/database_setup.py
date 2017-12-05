import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'email': self.email,
           'id': self.id,
           'picture': self.picture,
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    img_url = img_url = Column(String(500))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
           'img_url': self.img_url,
        }


class Teams(Base):
    __tablename__ = 'teams'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    yr_strtd = Column(String(4), nullable=False)
    image_url = Column(String(500))
    location = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
           'image_url': self.image_url,
           'yr_strtd': self.yr_strtd,
           'location': self.location,
        }

engine = create_engine('sqlite:///itemcatalogwithuser.db')

Base.metadata.create_all(engine)
