
import sys
import logging


logger = logging.getLogger('nerus')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

log = logger.info
log_error = logger.error


def dot():
    print('.', end='', file=sys.stderr, flush=True)


def log_progress(items, prefix=None, total=None):
    from tqdm import tqdm

    # https://github.com/tqdm/tqdm/issues/461#issuecomment-334343230
    tqdm.get_lock().locks = []
    return tqdm(items, desc=prefix, total=total)
