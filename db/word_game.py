import datetime
from typing import Optional

from misc import db
from models.users import User
from models.word_game import WordGameForm, WordGame

TABLE = "word_game"


async def create_game(
        conn: db.Connection,
        user: User
) -> Optional[WordGame]:
    word_game = WordGameForm(
        user_id=user.user_id,
        ctime=datetime.datetime.now()
    )
    result = await db.create(conn, TABLE, word_game.dict())
    return db.record_to_model(WordGame, result)


async def get_game_by_user_id(
        conn: db.Connection,
        user_id: int
) -> Optional[WordGame]:
    values = [user_id]
    where = "user_id=$1 AND is_finished=FALSE"
    record = await db.get_by_where(
        conn,
        TABLE,
        where,
        values
    )
    return db.record_to_model(WordGame, record)


async def make_game_finished(
        conn: db.Connection,
        word_game: WordGame
) -> Optional[WordGame]:
    word_game.etime = datetime.datetime.now()
    word_game.is_finished = True
    result = await db.update(
        conn,
        TABLE,
        word_game.id,
        word_game.dict()
    )
    return db.record_to_model(WordGame, result)
