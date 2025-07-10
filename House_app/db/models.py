from typing import Optional
from sqlalchemy import Text,Integer, String, Boolean, Enum, ForeignKey
from enum import Enum as PyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base



class LanguageChoices(PyEnum):
    RU = "ru"
    EN = "en"
    KY = "ky"


class ConditionChoices(PyEnum):
    NEW = "new"
    GOOD = "good"
    RENOVATED = "renovated"
    NEEDS_REPAIR = "needs_repair"


class User(Base):
    __tablename__= "users"

    id  :Mapped[int]= mapped_column(Integer,primary_key=True, autoincrement=True)
    user:Mapped [str]=mapped_column(String(50),unique=True,nullable=False)
    email:Mapped [str]=mapped_column(String(100), unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(255),nullable=False)
    phone_number:Mapped[str]=mapped_column(String(20),nullable=False)

    admin: Mapped[bool] =mapped_column(Boolean, default=False)
    seller:Mapped[bool]=mapped_column(Boolean,default=False)
    buyer:Mapped[bool]= mapped_column(Boolean,default=False)
    preferred_language: Mapped[LanguageChoices]= mapped_column(
        Enum(LanguageChoices,name="language_choices", native_enum=False),
        default=LanguageChoices.RU
    )


class Property(Base):
    __tablename__='properties'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_type: Mapped[Optional[str]] = mapped_column(String(50))
    region: Mapped[str]=mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    district: Mapped[Optional[str]] = mapped_column(String(50))
    address: Mapped[str]=mapped_column(String(255))
    area: Mapped[float]=mapped_column()
    price: Mapped[float]=mapped_column()
    rooms:Mapped[int]= mapped_column()
    floor: Mapped[int] =mapped_column()
    total_floors:Mapped[int]=mapped_column()
    condition:Mapped[ConditionChoices]=mapped_column(
        Enum(ConditionChoices,name='condition_choices', native_enum=False
             )
    )
    documents:Mapped[Optional[str]] =mapped_column(Text,nullable=True)
    seller:Mapped['User']=relationship('User', backref='properties')
    seller_id:Mapped[int]=mapped_column(ForeignKey('users.id'))


class Review(Base):
    __tablename__='reviews'
    id: Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    author_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    seller_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    rating:Mapped[int] =mapped_column(Integer)
    created_at:Mapped[datetime]=mapped_column(default=datetime.utcnow)

    author: Mapped["User"] = relationship("User", foreign_keys=[author_id], backref="written_reviews")
    seller: Mapped["User"] = relationship("User", foreign_keys=[seller_id], backref="received_reviews")