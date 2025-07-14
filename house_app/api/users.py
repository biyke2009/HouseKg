from house_app.db.database import SessionLocale
from house_app.db.models import User
from house_app.db.schemas import  UserSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends,APIRouter
from typing import List



user_router = APIRouter(prefix="/users", tags=["Users"])

async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()

@user_router.get('/',response_model=List[UserSchema])
async def get_users(db:Session =Depends(get_db)):
    return db.query(User).all()


@user_router.get('/{user_id}', response_model=UserSchema)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user =db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail='Пользователь не найден')
    return user


@user_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    db.delete(user)
    db.commit()
    return {'message': 'Пользователь удалён'}
