import asyncio
import json
import logging
import os

from asyncpg import UniqueViolationError

from db import words
from misc import db
from models.words import WordForm

logger = logging.getLogger(__name__)


def read_config(path):
    if not os.path.exists(path):
        logger.error(f'Config file not found at {path}')
        return None
    with open(path, 'r') as fd:
        return json.load(fd)


async def run():
    config_path = os.environ['SRVC_CONFIG']
    conf = read_config(config_path)

    if os.path.exists("words.txt"):
        with open("words.txt", "r") as file:
            db_pool = await db.get_conn(conf['db'])
            words_file = file.readlines()
            words_forms = [WordForm(word=word.lower().rstrip()) for word in words_file]
            try:
                await words.create_many_words(db_pool, words_forms)
            except UniqueViolationError:
                pass
            await db.close(db_pool)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


