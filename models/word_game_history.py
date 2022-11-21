import datetime
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    Field
)


class AnswerSource(str, Enum):
    USER = 'user'
    BOT = 'bot'


class WordGameHistoryForm(BaseModel):
    game_id: int
    word_id: int
    answer_source: AnswerSource


class WordGameHistory(BaseModel):
    id: int
    game_id: int
    word_id: int
    answer_source: AnswerSource
    ctime: Optional[datetime.datetime] = Field(None, nullable=True)
