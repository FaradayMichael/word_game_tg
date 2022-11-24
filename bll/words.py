from typing import Optional
import logging

from db.word_game_history import get_words_ids_by_game_query, get_last_history_record
from db.words import TABLE as WORDS_TABLE, get_word, get_word_by_id
from db.word_game_history import TABLE as HISTORY_TABLE
from misc import db
from models.word_game import WordGame
from models.words import Word

logger = logging.getLogger(__name__)


async def find_answer_word_by_letter(
        conn: db.Connection,
        letter: str,
        game: WordGame,
) -> Optional[Word]:
    values = [game.id, game.difficulty]

    game_words_ids_query = get_words_ids_by_game_query()
    query = f"SELECT * FROM {WORDS_TABLE} " \
            f"WHERE id NOT IN ({game_words_ids_query}) " \
            f"AND difficulty <= $2 " \
            f"AND word SIMILAR TO '{letter}%' " \
            f"ORDER BY random() " \
            f"LIMIT 1"
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(Word, result)


async def is_word_already_in_history(
        conn: db.Connection,
        word: Word,
        game: WordGame
) -> bool:
    values = [game.id, word.id]
    query = f"SELECT * FROM {HISTORY_TABLE} " \
            f"WHERE game_id=$1 AND word_id=$2"
    result = await conn.fetch(query, *values)
    return bool(result)


async def is_word_follow_rules(
        conn: db.Connection,
        word: Word,
        game: WordGame
) -> bool:
    last_word = await get_last_game_word(conn, game)
    if last_word is not None:
        return last_word.word[-1] == word.word[0]
    else:
        return True


async def get_last_game_word(
        conn: db.Connection,
        game: WordGame
) -> Optional[Word]:
    last_history_record = await get_last_history_record(conn, game.id)
    if last_history_record is not None:
        return await get_word_by_id(conn, last_history_record.word_id)
    else:
        return None
