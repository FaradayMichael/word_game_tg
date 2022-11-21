import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field
)

from models.users import User


class WordGameForm(BaseModel):
    ctime: Optional[datetime.datetime] = Field(None, nullable=True)
    etime: Optional[datetime.datetime] = Field(None, nullable=True)
    user_id: int
    is_finished: bool = False


class WordGame(WordGameForm):
    id: int
