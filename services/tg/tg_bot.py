from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from misc.aiogram import MainDispatcher
from .handlers.base import send_on_start
from .handlers.word_game import (
    send_on_start_game,
    send_rules,
    send_on_stop_game,
    send_on_end_game,
    handle_answer,
    create_game
)
from .fsm import FSM_create_game


class State(object):
    def __init__(self, conf: dict):
        super().__init__()
        self.conf = conf
        self.bot = Bot(token=conf["tg_token"])
        self.dp = MainDispatcher(self.bot, storage=MemoryStorage())
        self.dp.config = self.conf


def init(conf: dict) -> State:
    state = State(conf)
    register(state)
    return state


def register(state: State):
    state.dp.register_message_handler(
        send_on_start,
        commands=["start", 'старт'],
        state='*'
    )
    state.dp.register_message_handler(
        send_on_start_game,
        commands=["start_game"],
        state='*'
    )
    state.dp.register_message_handler(
        send_on_stop_game,
        commands=["stop_game"],
        state='*'
    )
    state.dp.register_message_handler(
        send_rules,
        commands=["rules"],
        state='*'
    )
    state.dp.register_message_handler(
        create_game,
        state=FSM_create_game.difficulty
    )
    state.dp.register_message_handler(
        handle_answer,
        state='*'
    )

