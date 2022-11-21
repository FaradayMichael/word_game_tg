from aiogram import types
import random

from bll.users import get_or_create_user
from bll.word_game_base import get_answer_word
from bll.words import is_word_already_in_history, is_word_follow_rules, get_last_game_word
from db import (
    words,
    word_game,
    word_game_history
)
from db.word_game_history import get_last_history_record, create_game_history
from misc.aiogram import MainDispatcher
from models.word_game_history import WordGameHistoryForm, AnswerSource


async def send_rules(msg: types.Message):
    await msg.answer(f"ajajaja")


async def send_on_start_game(msg: types.Message):
    dp = MainDispatcher.get_current()
    conn = dp.db_pool

    user = await get_or_create_user(conn, msg.from_user.id)

    game = await word_game.get_game_by_user_id(conn, user.user_id)
    if game is None:
        game = await word_game.create_game(conn, user)
        await msg.answer(f"Game created {game.id}")
        # if random.getrandbits(1):
        if True:
            await msg.answer("Your turn")
    else:
        await msg.answer("Game has already started")


async def send_on_stop_game(msg: types.Message):
    dp = MainDispatcher.get_current()
    conn = dp.db_pool

    user = await get_or_create_user(conn, msg.from_user.id)

    game = await word_game.get_game_by_user_id(conn, user.user_id)
    if game is not None:
        await word_game.make_game_finished(conn, game)
        await send_on_end_game(msg)


async def send_on_end_game(msg: types.Message):
    await msg.answer("Game successfully ended ")


async def handle_answer(msg: types.Message):
    dp = MainDispatcher.get_current()
    conn = dp.db_pool
    user = await get_or_create_user(conn, msg.from_user.id)

    game = await word_game.get_game_by_user_id(conn, user.user_id)
    if game is not None:
        word = await words.get_word(conn, msg.text.lower())
        if word is None:
            return await msg.answer(f"Word {msg.text} does not exist")
        if await is_word_already_in_history(conn, word, game):
            return await msg.answer(f"Word {word.word} has already been!")
        if not await is_word_follow_rules(conn, word, game):
            last_word = await get_last_game_word(conn, game)
            return await msg.answer(
                f"Word {word.word[0:-1]}{word.word[-1].upper()} "
                f"does not complement word {last_word.word[0].upper()}{last_word.word[1:]}"
            )
        await create_game_history(
            conn,
            WordGameHistoryForm(
                game_id=game.id,
                word_id=word.id,
                answer_source=AnswerSource.USER
            )
        )

        answer_word = await get_answer_word(conn, word, game)

        if answer_word is not None:
            await create_game_history(
                conn,
                WordGameHistoryForm(
                    game_id=game.id,
                    word_id=answer_word.id,
                    answer_source=AnswerSource.BOT
                )
            )
            await msg.answer(answer_word.word)
        else:
            await msg.answer("U won")
            return await send_on_end_game(msg)
