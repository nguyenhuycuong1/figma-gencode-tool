from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User


class UserRepository:
    def create(self, user_create: UserCreate, db: Session):
        if self.exists_email(user_create.email, db):
            raise HTTPException(status_code=400, detail="Email already exists")
        user = User(email=user_create.email, password_hash=user_create.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def exists_email(self, email: str, db: Session) -> bool:
        return db.query(User).filter(User.email == email).first() is not None

    def get_user_by_email(self, email: str, db: Session) -> type[User]:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_id(self, user_id: UUID, db: Session) -> type[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_all(self, db: Session):
        return db.query(User).all()