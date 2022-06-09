from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from crud import (
    create_user, 
    get_user_by_email, 
    get_user_by_id,
    delete_user_by_id,
    get_user_list
)
from schemas import UserRequest,UserUpdate
from fastapi.responses import Response
from tasks import update_address_coord
from fastapi.encoders import jsonable_encoder
from geopy.distance import geodesic

models.Base.metadata.create_all(bind=engine)

# App - Fastapi
app = FastAPI(
    title="Location Finder",
    description="A simple Location Finding application built with FastAPI",
    version="1"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Creating User with his/her Address
@app.post("/users/")
async def create_user_(user: UserRequest, db: Session = Depends(get_db)):
    mail = user.email
    db_user = get_user_by_email(db, email=mail)
    if db_user.count():
        raise HTTPException(status_code=400, detail="Email '{}' already registered".format(mail))
    return create_user(db=db, user=user)

# Updating User object
@app.put("/users/{user_id}/",response_model=UserUpdate)
async def update_user_(tasks:BackgroundTasks, user: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user.count():
        db_user = db_user.first()
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            if key=="address":
                tasks.add_task(update_address_coord,db_user,db)
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return jsonable_encoder(db_user)
    raise HTTPException(status_code=404, detail="No User Data Found")

# Deleting User object
@app.delete("/users/{user_id}/")
async def delete_user_(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user.count():
        db_user = db_user.first()
        delete_user_by_id(db,db_user)
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="No User Data Found")

# Deleting Address Objects using distance parameter
@app.get("/users/")
async def get_users(distance: int=0, lat: float=0.0,long:float=0.0,db: Session = Depends(get_db)):
    db_users = get_user_list(db)
    if db_users:
        if (distance and (lat and long)):
            coordinates = [lat,long]
            near_locations = list()
            for user in db_users:
                user_coord = [user.lat,user.long]
                if geodesic(user_coord,coordinates).km <= distance:
                    near_locations.append(user)
            return near_locations
        else:
            return db_users
    raise HTTPException(status_code=404, detail="No User Data Found")
