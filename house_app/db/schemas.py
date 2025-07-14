from pydantic import BaseModel, EmailStr,conint
from typing import List,Optional
from datetime import datetime
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

class RoleChoices(str,Enum):
    admin = 'admin'
    seller= 'seller'
    buyer='buyer'

class LanguageChoices(str, Enum):
    en='en'
    ru='ru'
    ky='ky'

class SellerSchema(BaseModel):
    id:int
    user:str


class ConditionChoices(str,Enum):
    new='new'
    good= 'good'
    needs_repair='needs_repair'
    renovated='renovated'

class DocumentSchema(BaseModel):
    id: Optional[int]
    url: str


class UserSchema(BaseModel):
    id:int
    email:EmailStr
    password:str
    phone_number:Optional[int]
    preferred_language: LanguageChoices

    class Config:
        from_attributes=True


class PropertySchema(BaseModel):
    title:str
    description: Optional[str]
    property_type:Optional[str]
    region: str
    city: str
    district: Optional[str]
    address: str
    area: float
    price:float
    rooms: int
    floor: int
    total_floors: int
    condition:ConditionChoices
    documents:List[DocumentSchema] = []
    seller:SellerSchema


class ReviewSchema(BaseModel):
    author: int
    seller:int
    comment:Optional[str]=None
    rating: conint(ge=1, le=5)

    class Config:
        from_attributes=True