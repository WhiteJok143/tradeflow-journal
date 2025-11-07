from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://tfj_user:tfj_pass@localhost:5432/tfj_db')


Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
__tablename__ = 'users'
id = Column(Integer, primary_key=True, index=True)
email = Column(String, unique=True, index=True, nullable=False)
hashed_password = Column(String, nullable=False)
role = Column(String, default='user')
created_at = Column(DateTime, default=datetime.utcnow)
is_active = Column(Boolean, default=True)
accounts = relationship('Account', back_populates='user')


class Account(Base):
__tablename__ = 'accounts'
id = Column(Integer, primary_key=True, index=True)
user_id = Column(Integer, ForeignKey('users.id'))
broker = Column(String, nullable=True)
login = Column(String, nullable=True)
server = Column(String, nullable=True)
user = relationship('User', back_populates='accounts')
trades = relationship('Trade', back_populates='account')


class Trade(Base):
__tablename__ = 'trades'
id = Column(Integer, primary_key=True, index=True)
account_id = Column(Integer, ForeignKey('accounts.id'))
ticket = Column(String, index=True)
symbol = Column(String)
open_time = Column(DateTime)
close_time = Column(DateTime)
volume = Column(Float)
profit = Column(Float)
comment = Column(String, nullable=True)
account = relationship('Account', back_populates='trades')
