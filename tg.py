import json
import logging
import os

from services.tg.main import run

logger = logging.getLogger(__name__)


def read_config(path):
    if not os.path.exists(path):
        logger.error(f'Config file not found at {path}')
        return None
    with open(path, 'r') as fd:
        return json.load(fd)


if __name__ == '__main__':
    config_path = os.environ['SRVC_CONFIG']
    conf = read_config(config_path)
    run(conf)
