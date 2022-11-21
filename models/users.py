import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    name: str = None
    ctime: Optional[datetime.datetime] = Field(None, nullable=True)