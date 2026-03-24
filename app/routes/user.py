from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.middleware.sessions import Session

from app.core.db import get_db
from app.schemas.user import UserCreate
from app.services.user import UserService

def get_user_service():
    return UserService()

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
def create_user(user_create: UserCreate, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.save_user(user_create, db)

@router.get("/")
def read_users(db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users(db)