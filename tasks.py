from sqlalchemy.orm import Session
import models
from geo_coder import convert_address_coord

# Background Task for updating Co-ordinates according to address
async def update_address_coord(db_user: models.User, db: Session):
    for key, value in convert_address_coord(db_user.address).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()