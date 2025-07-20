import logging

from svcutils.service import get_work_dir, setup_logging

NAME = 'bfshuffle'
WORK_DIR = get_work_dir(NAME)
logger = logging.getLogger(NAME)
setup_logging(path=WORK_DIR, name=NAME)
logging.getLogger('asyncio').setLevel(logging.INFO)
