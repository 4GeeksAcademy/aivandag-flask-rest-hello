from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

posts: Mapped[list['Post']] = relationship('Post', back_populates='user', cascade='all, delete-orphan')
comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user', cascade='all, delete-orphan')
likes: Mapped[list['Like']] = relationship('Like', back_populates='user', cascade='all, delete-orphan')

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