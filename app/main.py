import os
from datetime import datetime, timedelta
from typing import Optional, List


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session


from .models import Base, engine, SessionLocal, User, Account, Trade
from .schemas import UserCreate, Token, TradeIn
from .auth import verify_password, get_password_hash, create_access_token
from .crud import get_user_by_email, create_user, get_or_create_account, trade_exists, create_trade


# Инициализация DB (если нужно создать таблицы вручную)
Base.metadata.create_all(bind=engine)


app = FastAPI(title='TradeFlow Journal')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Auth helpers
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from .auth import decode_token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    email = payload.get('sub')
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


# Admin guard
def admin_required(user: User = Depends(get_current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admin privileges required')
    return user


# Routes
@app.post('/register')
def register(u: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, u.email):
        raise HTTPException(status_code=400, detail='Email already registered')
    user = create_user(db, u.email, get_password_hash(u.password))
    return {'msg': 'user created', 'email': user.email}


@app.post('/token', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}




@app.get("/me")
def read_me(current_user: User = Depends(get_current_active_user)):
    return {"email": current_user.email, "role": current_user.role}

