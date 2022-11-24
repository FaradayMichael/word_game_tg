from aiogram.dispatcher.filters.state import State, StatesGroup


class FSM_create_game(StatesGroup):
    difficulty = State()
