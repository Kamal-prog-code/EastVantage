from sqlalchemy import Boolean, Column, Integer, String, Numeric

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)
    is_active = Column(Boolean, default=True)
    lat = Column(Numeric(3,15))
    long = Column(Numeric(3,15))