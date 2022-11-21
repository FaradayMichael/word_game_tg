from typing import Optional

from bll.words import find_answer_word_by_letter
from misc import db
from models.word_game import WordGame
from models.words import Word


async def get_answer_word(
        conn: db.Connection,
        word: Word,
        game: WordGame
) -> Optional[Word]:
    answer_word = await find_answer_word_by_letter(
        conn,
        word.word.strip()[-1],
        game
    )
    return answer_word


