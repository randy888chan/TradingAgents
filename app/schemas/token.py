from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None # 'sub' is standard for subject (user identifier)
    # Add any other data you want to store in the token payload
    # For example, roles, permissions, etc.
    # email: Optional[str] = None
    # exp: Optional[int] = None # Already handled by create_access_token's expiry logic
