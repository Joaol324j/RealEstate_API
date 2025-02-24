from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime  
from app.core.auth import get_password_hash
from app.database import get_db  
from app.models import PasswordResetToken, User  
from app.crud import create_password_reset_token
from app.utils.email_service import send_password_reset_email
from app.validators import valid_email, strong_password

router = APIRouter(prefix="/reset", tags=["Reset"])

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    if not valid_email(email):
        raise HTTPException(status_code=400, detail="E-mail inválido.")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    reset_token = create_password_reset_token(db, user)
    reset_link = f"http://localhost:8000/reset/reset-password?token={reset_token.token}"

    send_password_reset_email(user.email, reset_link)

    return {"message": "E-mail de recuperação enviado!"}

@router.post("/")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    
    if not reset_token:
        raise HTTPException(status_code=400, detail="Token inválido.")
    
    if reset_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado.")
    
    if not strong_password(new_password):
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, um número e um caractere especial")
    
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    user.hashed_password = get_password_hash(new_password)
    db.delete(reset_token)  
    db.commit()

    return {"message": "Senha redefinida com sucesso!"}
