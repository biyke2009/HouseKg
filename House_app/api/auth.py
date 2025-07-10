from House_app.db.schemas import Token
from House_app.utils.security import verify_password
from House_app.db.database import SessionLocale
from House_app.db.models import User
from House_app.db.schemas import UserSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends,APIRouter
from typing import List, Optional
from fastapi.security import ( OAuth2PasswordBearer,
                               OAuth2PasswordRequestForm)
from jose import jwt
from datetime import datetime,timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()

auth_router=APIRouter(prefix='/auth',tags=['/Auth'])


@auth_router.post("/register", response_model=dict)
def register(user: UserSchema, db: Session = Depends(get_db),hash_password=None):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_pw = hash_password(user.password)

    new_user = User(
        email=user.email,
        password=hashed_pw,
        phone_number=user.phone_number,
        admin=user.admin,
        seller=user.seller,
        buyer=user.buyer,
        preferred_language=user.preferred_language
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Пользователь успешно зарегистрирован", "user_id": new_user.id}


@auth_router.post('/login', response_model=Token)
def login (form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise  HTTPException(status_code=404,detail='Неверный email или пароль')


@auth_router.get('/me')
def read_users_me(current_user: User = Depends(get_db)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "phone": current_user.phone_number,
        "language": current_user.preferred_language,
        "admin": current_user.admin,
        "seller": current_user.seller,
        "buyer": current_user.buyer
    }