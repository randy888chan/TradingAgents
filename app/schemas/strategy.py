from pydantic import BaseModel
from typing import Optional, Dict, Any

class StrategyBase(BaseModel):
    name: str
    algorithm: Optional[str] = None
    params: Optional[Dict[str, Any]] = None

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(StrategyBase):
    pass

class StrategyInDBBase(StrategyBase):
    id: int
    user_id: int # Assuming strategies are linked to users

    class Config:
        orm_mode = True # For Pydantic v1 compatibility

class Strategy(StrategyInDBBase):
    status: Optional[str] = "stopped" # Example field

class StrategyInDB(StrategyInDBBase):
    pass
