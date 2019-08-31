
from nerus.log import (
    dot,
    log,
    log_error
)
from nerus.path import basename
from nerus.worker import run as worker_run_
from nerus.yc import (
    get_sdk,
    find_folder,
    find_instance,
    create_instance,
    remove_instance,
    instance_ip
)
from nerus.ssh import (
    get_client,
    exec as ssh_exec,
    upload,
    download
)
from nerus.const import (
    WORKER_NAME,
    WORKER_HOST,

    YC_HDD,
    YC_UBUNTU_1604
)


#######
#
#   RUN
#
#######


def worker_run(args):
    log('Starting worker')
    worker_run_()


#######
#
#   CREATE
#
#########


CONFIG = dict(
    cores=16,
    share=100,
    memory=16,
    disk_size=50,
    disk_type=YC_HDD,
    image=YC_UBUNTU_1604,
    spot=True,
)


def find_worker(sdk, name=WORKER_NAME):
    folder = find_folder(sdk)
    return find_instance(sdk, folder, name)


def worker_create(args):
    worker_create_()


def worker_create_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if instance:
        log_error('Worker already exists')
        return

    log('Creating worker')
    for key in sorted(CONFIG):
        log('  %s: %s' % (key, CONFIG[key]))

    create_instance(
        sdk,
        name=WORKER_NAME,
        callback=dot,
        **CONFIG
    )
    ip = worker_ip__()
    log('Worker ip: %s' % ip)


########
#
#   IP
#
########


def worker_ip(args):
    worker_ip_()


def worker_ip_():
    ip = worker_ip__()
    if ip:
        print(ip)


def worker_ip__():
    log('Listing instances')
    sdk = get_sdk()
    instance = find_worker(sdk)
    if not instance:
        log_error('No worker')
        return

    ip = instance_ip(instance)
    if not ip:
        log_error('No ip (yet?)')
        return

    return ip


########
#
#   SSH
#
############


def worker_ssh(args):
    worker_ssh_(args.command)


def worker_ssh_(command, host=WORKER_HOST):
    client = get_client(host)
    log('[%s] %r' % (host, command))
    ssh_exec(client, command)


########
#
#   TRANSFER
#
##########


def worker_upload(args):
    worker_transfer(upload, args.source, args.target)


def worker_download(args):
    worker_transfer(download, args.source, args.target)


def worker_transfer(method, source, target=None, host=WORKER_HOST):
    if not target:
        target = basename(source)

    client = get_client(host)
    log('%s %s -> %s', method.__name__, source, target)
    try:
        method(client, source, target)
    except FileNotFoundError as error:
        log_error(error)


#######
#
#   REMOVE
#
#######


def worker_remove(args):
    worker_remove_()


def worker_remove_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if instance:
        log('Removing worker')
        remove_instance(sdk, instance, dot)
    else:
        log_error('No worker')
