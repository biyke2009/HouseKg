from house_app.db.database import SessionLocale
from house_app.db.models import Property
from house_app.db.schemas import  PropertySchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends,APIRouter
from typing import List

property_router=APIRouter(prefix='/properties',tags=['Properties'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


@property_router.post('/',response_model=PropertySchema)
async def create_property(property_data:PropertySchema, db: Session =Depends(get_db)):

    new_property =db.query(Property).filter(Property.user_id).frist()
    if not property:
        db.add(property)
        db.commit()
        db.refresh(property)


@property_router.get('/property_id', response_model=PropertySchema)
async def get_property(property_id:int, db:Session=Depends(get_db)):
    property_obj= db.query(Property).filter(Property.id== property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404,detail='Недвижимость не найдена')
    return property_obj