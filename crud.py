from sqlalchemy.orm import Session
from geo_coder import convert_address_coord
import models, schemas

# Create User object
def create_user(db: Session, user: schemas.UserRequest):
    db_user = models.User(email=user.email,address=user.address)
    for key, value in convert_address_coord(user.address).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Retrieve User object by email
def get_user_by_email(db: Session, email: str):
    query = db.query(models.User).filter(models.User.email == email)
    return query

# Retrieve User object by id
def get_user_by_id(db: Session, user_id: int):
    query = db.query(models.User).filter(models.User.id == user_id)
    return query

# Delete User object by id
def delete_user_by_id(db: Session,db_user: models.User):
    db.delete(db_user)
    db.commit()
    return 1     

# Retrieve Users List
def get_user_list(db: Session):
    query = db.query(models.User).all()
    return query

