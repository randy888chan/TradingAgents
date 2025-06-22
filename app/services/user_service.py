from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate # Will be used for user creation later
from app.core.security import get_password_hash # For user creation

def get_user_by_email(db: Session, *, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Example of how to create a user (e.g., for a CLI command or initial setup script)
# This is not an API endpoint.
# def init_db_add_user(db: Session, email: str, password: str) -> User:
#     user = get_user_by_email(db, email=email)
#     if not user:
#         user_in = UserCreate(email=email, password=password)
#         user = create_user(db, user_in=user_in)
#         print(f"User {email} created.")
#         return user
#     print(f"User {email} already exists.")
#     return user
