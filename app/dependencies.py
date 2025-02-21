from fastapi import Depends, HTTPException, status
from app.models import User, UserRole
from app.core.auth import get_current_user

def verify_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas administradores podem realizar esta ação.")
    return user