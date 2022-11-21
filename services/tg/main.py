import logging
from aiogram import executor

from misc import db
from misc.aiogram import MainDispatcher
from services.tg import tg_bot

logger = logging.getLogger(__name__)


def run(config):
    state = tg_bot.init(config)
    executor.start_polling(
        state.dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
    )


async def on_startup(dp: MainDispatcher):
    dp.db_pool = await db.init(dp.config['db'])


async def on_shutdown(dp: MainDispatcher):
    await db.close(dp.db_pool)
