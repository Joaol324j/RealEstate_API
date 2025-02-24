from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserCreate, UserOut
from app.crud import get_user, create_user
from app.validators import valid_email, strong_password, valid_username, valid_phone
from app.core.auth import get_current_user
from app.models import UserRole

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if not valid_email(user.email):
        raise HTTPException(status_code=400, detail="Formato de e-mail inválido")
    
    if not strong_password(user.password):
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, um número e um caractere especial")
    
    if not valid_username(user.username):
        raise HTTPException(status_code=400, detail="O nome de usuário deve ter entre 3 e 20 caracteres e pode conter apenas letras, números e underscores")
    
    if not valid_phone(user.telephone):
        raise HTTPException(status_code=400, detail="Número de telefone inválido")

    existing_user = await get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return await create_user(db, user)

@router.post("/register/admin", response_model=UserOut)
async def register_admin(user: UserCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    if not valid_email(user.email):
        raise HTTPException(status_code=400, detail="Formato de e-mail inválido")
    
    if not strong_password(user.password):
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, um número e um caractere especial")
    
    if not valid_username(user.username):
        raise HTTPException(status_code=400, detail="O nome de usuário deve ter entre 3 e 20 caracteres e pode conter apenas letras, números e underscores")
    
    if not valid_phone(user.telephone):
        raise HTTPException(status_code=400, detail="Número de telefone inválido")

    existing_user = await get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    return await create_user(db, user, role=UserRole.admin)