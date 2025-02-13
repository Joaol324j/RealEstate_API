from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserCreate, UserOut
from app.crud import get_user, create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return await create_user(db, user)