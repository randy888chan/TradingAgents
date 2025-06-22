from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.schemas.token import Token
from app.db.session import get_db
# We'll create user_service.py next for get_user_by_email
from app.services.user_service import get_user_by_email
from app.models.user import User as UserModel # To avoid confusion with pydantic User schema

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username) # OAuth2 form uses 'username' for email
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email} # 'sub' is the subject of the token (user's email)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Placeholder for user creation - to be developed further if needed for testing
# This is NOT a production-ready registration endpoint.
# from app.schemas.user import UserCreate
# from app.core.security import get_password_hash
# @router.post("/register", response_model=UserSchema) # Assuming UserSchema is your Pydantic model for User response
# def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_email(db, email=user_in.email)
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered",
#         )
#     hashed_password = get_password_hash(user_in.password)
#     db_user = UserModel(email=user_in.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
