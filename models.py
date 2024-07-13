from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class Chat(Base):
    __tablename__ = "Chat"
    chat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    user = relationship("User")

class ChatContent(Base):
    __tablename__ = "Chat_content"
    message_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('Chat.chat_id'))
    message_content = Column(Text, nullable=False)
    message_type = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    chat = relationship("Chat")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserInput(BaseModel):
    text: str

class Token(BaseModel):
    access_token: str
    token_type: str
