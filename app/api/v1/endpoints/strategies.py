from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.schemas.strategy import Strategy
from app.schemas.token import TokenPayload
from app.db.session import get_db
from app.services.user_service import get_user_by_email
from app.models.user import User as UserModel
from app.core.security import decode_access_token
from app.core.config import settings


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserModel:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials (payload missing)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str | None = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials (email missing in token)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/", response_model=List[Strategy])
async def read_strategies(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Retrieve strategies for the current user.
    This is a dummy endpoint and returns a hardcoded list.
    """
    # In a real application, you would fetch strategies for current_user.id from the database
    dummy_strategies = [
        Strategy(id=1, name="DQN_Long_BTC", algorithm="DQN", user_id=current_user.id, status="running", params={"symbol": "BTC/USDT"}),
        Strategy(id=2, name="PPO_Short_ETH", algorithm="PPO", user_id=current_user.id, status="stopped", params={"symbol": "ETH/USDT"}),
    ]
    return dummy_strategies
