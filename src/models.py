from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
import enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

posts: Mapped[list['Post']] = relationship('Post', back_populates='user', cascade='all, delete-orphan')
comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user', cascade='all, delete-orphan')
likes: Mapped[list['Like']] = relationship('Like', back_populates='user', cascade='all, delete-orphan')

followers: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='followed', cascade='all,delete-orphan')
followings: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower', cascade='all,delete-orphan')

def serialize(self):
    return {
        "id": self.id,
        "email": self.email,
        "is_active": self.is_active
            # do not serialize the password, its a security breach
    }


class Post(db.Model):
    __tablename__= 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]= mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped[list['User']] = relationship('User', back_populates='post', cascade='all, delete-orphan')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='post', cascade='all, delete-orphan')
    media: Mapped[list['Media']] = relationship('Media', back_populates='post', cascade='all, delete-orphan')

def serialize(self):
        return {
           "id": self.id,
           "user_id": self.user_id,
        }

class Comment(db.Model):
     __tablename__='comment'

     id: Mapped[int] = mapped_column(primary_key=True)
     post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
     text: Mapped[str] = mapped_column(String(350), nullable=False)

     user: Mapped[list['User']] = relationship('User', back_populates='comments', cascade='all, delete-orphan')
     posts: Mapped[list['Post']] = relationship('Post', back_populates='comments', cascade='all, delete-orphan')

def serialize(self):
    return {
        "id": self.id,
        "post_id": self.post_id,
        "user_id": self.user_id,
        "text": self.text,
        }

class Follower(db.Model):
     __tablename__= 'follower'

     user_from_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
     user_to_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)

     follower: Mapped['User'] = relationship('User', foreign_keys=[user_from_id], back_populates='followings')
     followed: Mapped['User'] = relationship('user', foreign_keys=[user_to_id], back_populates='followers')

     def serialize(self):
          return{
               "user_from_id": self.user_from_id,
               "user_to_id": self.user_to_id
          }
     
class MediaType(enum.Enum):
          IMAGE = 'image'
          VIDEO = 'video'
          GIF = 'gif'

class Media(db.Model):
     __tablename_= 'media'
     
     id: Mapped[int] = mapped_column(primary_key=True)
     type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
     url: Mapped[str] = mapped_column(String(300), nullable=False)
     post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

     post: Mapped["Post"] = relationship('Post', back_populates='media')

     def serialize(self):
          return{
               "id": self.id,
               'type': self.type.value,
               'url': self.url,
               'post_id': self.post_id

          }
    

class Like(db.Model):
     __tablename__ = 'like'

     id: Mapped[int] = mapped_column(primary_key=True)
     post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

     user: Mapped[list['User']] = relationship('User', back_populates='likes', cascade='all, delete-orphan')
     posts: Mapped[list['Post']] = relationship('Post', back_populates='likes', cascade='all, delete-orphan')
     
def serialize(self):
    return {
        "id": self.id,
        "post_id": self.post_id,
        "user_id": self.user_id,
    }