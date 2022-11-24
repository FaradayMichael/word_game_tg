from pydantic import BaseModel


class WordForm(BaseModel):
    word: str
    difficulty: int


class Word(WordForm):
    id: int
