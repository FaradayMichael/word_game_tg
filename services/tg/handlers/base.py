from aiogram import types

from bll.users import get_or_create_user
from misc.aiogram import MainDispatcher


async def send_on_start(msg: types.Message):
    dp = MainDispatcher.get_current()
    conn = dp.db_pool

    user = await get_or_create_user(
        conn,
        msg.from_user.id,
        msg.from_user.full_name
    )
    await msg.answer(f"Hello, {user.name}")



