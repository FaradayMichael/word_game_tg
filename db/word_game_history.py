from typing import Optional

from misc import db
from models.word_game_history import WordGameHistoryForm, WordGameHistory

TABLE = "word_game_history"


def get_words_ids_by_game_query(
        value_id: int = None
) -> str:
    query = f"SELECT word_id FROM {TABLE} " \
            f"WHERE game_id=${value_id or 1}"
    return query


async def create_game_history(
        conn: db.Connection,
        game_history: WordGameHistoryForm
) -> Optional[WordGameHistory]:
    result = await db.create(conn, TABLE, game_history.dict())
    return db.record_to_model(WordGameHistory, result)


async def get_by_game_id(
        conn: db.Connection,
        game_id: int
) -> list[WordGameHistory]:
    values = [game_id]
    result = await db.get_list(
        conn=conn,
        table=TABLE,
        where=f"game_id=$1",
        values=values
    )
    return db.record_to_model_list(WordGameHistory, result)


async def get_last_history_record(
        conn: db.Connection,
        game_id: int
) -> Optional[WordGameHistory]:
    values = [game_id]
    query = f"SELECT * FROM {TABLE} " \
            f"WHERE game_id=$1 " \
            f"ORDER BY id DESC " \
            f"LIMIT 1"
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(WordGameHistory, result)