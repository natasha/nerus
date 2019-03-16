
from os import listdir as list_dir  # noqa
from os import remove as rm  # noqa
from os.path import exists  # noqa
from os.path import dirname as get_dir  # noqa
from os.path import basename  # noqa
from os.path import isdir as is_dir  # noqa
from os.path import join as join_path  # noqa
from os.path import normpath as norm_path  # noqa
from os.path import expanduser as expand_user  # noqa
from glob import iglob as list_paths  # noqa


def maybe_rm(path):
    if exists(path):
        rm(path)
