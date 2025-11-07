from sqlalchemy.orm import Session
from . import models


# Пользователи
def get_user_by_email(db: Session, email: str):
return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, email: str, hashed_password: str):
user = models.User(email=email, hashed_password=hashed_password)
db.add(user)
db.commit()
db.refresh(user)
return user


# Аккаунты
def get_or_create_account(db: Session, user_id: int, login: str):
acct = db.query(models.Account).filter(models.Account.login == login, models.Account.user_id == user_id).first()
if acct:
return acct
acct = models.Account(user_id=user_id, login=login)
db.add(acct)
db.commit()
db.refresh(acct)
return acct


# Сделки
def trade_exists(db: Session, ticket: str, account_id: int):
return db.query(models.Trade).filter(models.Trade.ticket == ticket, models.Trade.account_id == account_id).first()


def create_trade(db: Session, account_id: int, trade_data: dict):
trade = models.Trade(account_id=account_id, **trade_data)
db.add(trade)
db.commit()
db.refresh(trade)
return trade
