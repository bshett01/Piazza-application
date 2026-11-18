from ast import List
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func

from sqlalchemy import Column, Integer, String

from database import Base


# User describes the users table.
class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    
    # Each email must be unique because users log in with email.
    email = Column(String, unique=True, index=True, nullable=False)

    # Store the hashed password, never the original password.
    hashed_password = Column(String, nullable=False)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String,  nullable=False)
    status = Column(String, nullable=False, default="Live")
    body = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime,  nullable=False)
    

class PostTopic(Base):
    __tablename__ = "post_topics"

    post_id = Column(Integer, ForeignKey("post.id"),primary_key=True)
    topic_id = Column(String,  ForeignKey("topic.id"), primary_key=True)


class Topic(Base):
    __tablename__ = "topic"

    id = Column(String, primary_key=True)

    topic_name = Column(String, nullable=False)



