from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.auth import verify_password, create_access_token
from app.core.db import get_db
from app.schemas.token import Token

from app.services.user import UserService
from app.routes.user import get_user_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    username: str = form_data.username
    password: str = form_data.password

    user = user_service.get_user_by_email(email=username, db=db)
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}






