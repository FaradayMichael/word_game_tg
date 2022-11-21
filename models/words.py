from pydantic import BaseModel


class WordForm(BaseModel):
    word: str


class Word(WordForm):
    id: int
