from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole, Property
from app.schemas import PropertyCreate, PropertyUpdate

def create_property(db: Session, property_data: PropertyCreate):
    new_property = Property(**property_data.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

def get_all_properties(db: Session):
    return db.query(Property).all()

def get_property_by_id(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()

def update_property(db: Session, property_id: int, property_data: PropertyUpdate):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        return None
    for key, value in property_data.dict(exclude_unset=True).items():
        setattr(db_property, key, value)
    db.commit()
    db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int):
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        return None
    db.delete(db_property)
    db.commit()
    return db_property

async def get_user(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data, role: UserRole = UserRole.user):
    from app.core.auth import get_password_hash
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        telephone=user_data.telephone,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    return db_user