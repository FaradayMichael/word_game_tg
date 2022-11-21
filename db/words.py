from typing import Optional

from db.word_game_history import get_words_ids_by_game_query
from misc import db
from models.word_game import WordGame
from models.words import WordForm, Word

TABLE = 'words'


async def create_word(
        conn: db.Connection,
        word: WordForm
) -> Optional[Word]:
    result = await db.create(conn, TABLE, word.dict())
    return db.record_to_model(Word, result)


async def create_many_words(
        conn: db.Connection,
        words: list[WordForm]
):
    word_dicts = [word.dict() for word in words]
    await db.insert_many(conn, TABLE, word_dicts)


async def get_word_by_id(
        conn: db.Connection,
        id: int
) -> Optional[Word]:
    result = await db.get(conn, TABLE, id)
    return db.record_to_model(Word, result)


async def get_word(
        conn: db.Connection,
        word: str
) -> Optional[Word]:
    values = [word]
    result = await db.get_by_where(
        conn=conn,
        table=TABLE,
        where=f"word=$1",
        values=values
    )
    return db.record_to_model(Word, result)
