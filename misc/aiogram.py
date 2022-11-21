from typing import Type, T

from aiogram import Dispatcher

from misc import db


class MainDispatcher(Dispatcher):
    config: dict = None
    db_pool: db.Connection = None

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        return Dispatcher.get_current()

