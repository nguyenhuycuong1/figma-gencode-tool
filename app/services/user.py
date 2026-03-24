from uuid import UUID

from app.repositories.user_repository import UserRepository
from app.core.auth import hash_password
from app.schemas.user import UserCreate

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def save_user(self, user_create: UserCreate, db):
        password_hash = hash_password(user_create.password)
        user_create.password = password_hash
        print("hash_password", password_hash)
        return self.user_repo.create(user_create, db)

    def get_user_by_email(self, email: str, db):
        return self.user_repo.get_user_by_email(email, db)

    def get_user_by_id(self, user_id: UUID, db):
        return self.user_repo.get_user_by_id(user_id, db)

    def get_all_users(self, db):
        return self.user_repo.get_all(db)
    
    def get_current_user(self, user_id: UUID, db):
        return self.get_user_by_id(user_id, db)