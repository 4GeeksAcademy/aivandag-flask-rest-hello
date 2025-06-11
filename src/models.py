from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime, enum

db = SQLAlchemy()

class MediaType(enum.Enum):
     image = 'image'
     video = 'video'
     gif = 'gif'

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
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='author', cascade='all, delete-orphan')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='user', cascade='all, delete-orphan')
    media: Mapped[list['Media']] = relationship('Media', back_populates='post', cascade='all, delete-orphan')

    followers: Mapped[list['Follower']] = relationship('Follower', back_populates='followed', cascade='all, delete-orphan')
    following: Mapped[list['Follower']] = relationship('Follower', back_populates='follower', cascade='all, delete-orphan', foreign_keys='Follower.user_from_id')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
     __tablename__ = 'follower'
     
     user_from_id: Mapped[int] =mapped_column(ForeignKey('user.id'), primary_key=True)
     user_to_id: Mapped[int] =mapped_column(ForeignKey('user.id'), primary_key=True)

     follower: Mapped['User'] = relationship('User', foreign_key=[user_from_id], back_populates='following')
     followed: Mapped['User'] = relationship('User', foreign_key=[user_to_id], back_populates='followers')


class Post(db.Model):
    __tablename__= 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]= mapped_column(ForeignKey('user.id'), nullable=False)

user: Mapped[list['User']] = relationship('User', back_populates='posts', cascade='all, delete-orphan')
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
     text: Mapped[str] = mapped_column(String(350), nullable=False)
     author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

     author: Mapped['User'] = relationship('User', back_populates='comments', foreignkey=[author_id])
     posts: Mapped[list['Post']] = relationship('Post', back_populates='comments', cascade='all, delete-orphan')

def serialize(self):
    return {
        "id": self.id,
        "post_id": self.post_id,
        "author_id": self.author_id,
        "text": self.text,
        }

class Media(db.Model):
     __tablename__ = 'media'

     id: Mapped[int] = mapped_column(Integer, primary_key=True)
     type: Mapped[Media] = mapped_column(Enum,(Media), nullable=False)
     url: Mapped[str] = mapped_column(String(350), nullable=False)
     post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

     post: Mapped[['Post']] = relationship('Post', back_populates='media')

     
def serialize(self):
    return {
        "id": self.id,
        "post_id": self.post_id,
        "type": self.type.value,
        'url': self.url,
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