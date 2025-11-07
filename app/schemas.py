from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
email: EmailStr
password: str


class Token(BaseModel):
access_token: str
token_type: str


class TradeIn(BaseModel):
ticket: str
symbol: str
open_time: datetime
close_time: datetime
volume: float
profit: float
comment: Optional[str] = None
account_login: Optional[str] = None
