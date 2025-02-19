from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole
from app.schemas import UserCreate

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