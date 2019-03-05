
import sys
import logging

from tqdm import tqdm


logger = logging.getLogger('nerus')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

log = logger.info


def dot():
    print('.', end='', file=sys.stderr, flush=True)


def log_progress(items, label=None, hide=False):
    # https://github.com/tqdm/tqdm/issues/461#issuecomment-334343230
    tqdm.get_lock().locks = []
    return tqdm(items, desc=label, leave=not hide)
