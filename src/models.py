import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email_address = Column(String(250), unique=True, nullable=False)

class FollowedProfile(Base):
    __tablename__ = 'FollowedProfile'
    follower_id = Column(Integer, ForeignKey('profile.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('profile.id'), primary_key=True)
    follower = relationship('Profile', foreign_keys=[follower_id])
    followed = relationship('Profile', foreign_keys=[followed_id])

class PostContent(Base):
    __tablename__ = 'post_content'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('profile.id'), nullable=False)
    author = relationship('Profile', back_populates="posts")
    media_files = relationship('MediaFile', back_populates="post")
    comments = relationship('Comment', back_populates="post")

class MediaFile(Base):
    __tablename__ = 'media_file'
    id = Column(Integer, primary_key=True)
    file_type = Column(String(50), nullable=False) 
    file_url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post_content.id'), nullable=False)
    post = relationship('PostContent', back_populates="media_files")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    commenter_id = Column(Integer, ForeignKey('profile.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post_content.id'), nullable=False)
    commenter = relationship('Profile')
    post = relationship('PostContent', back_populates="comments")

    
class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('profile.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post_content.id'), nullable=False)
    user = relationship('Profile')
    post = relationship('PostContent', back_populates="likes")
    
Profile.posts = relationship('PostContent', back_populates="author")

def to_dict(self):
    return {}


try:
    render_er(Base, 'diagram.png')
    print("Diagram successfully generated! Check diagram.png.")
except Exception as e:
    print("An error occurred while generating the diagram:", e)
