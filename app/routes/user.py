from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status
from starlette.middleware.sessions import Session

from app.core.auth import get_current_user_id
from app.core.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

def get_user_service():
    return UserService()

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user_create: UserCreate, db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.save_user(user_create, db)

@router.get("/")
def read_users(db: Session = Depends(get_db), user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users(db)

@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db), 
    user_service: UserService = Depends(get_user_service)
    ):
    return user_service.get_current_user(user_id, db)