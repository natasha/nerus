
from nerus.log import log, dot
from nerus.worker import (
    run as run_worker_,
    deploy as deploy_worker__,
    CONFIG as WORKER_CONFIG
)
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
    exec as ssh_exec
)
from nerus.const import WORKER_NAME


def run_worker(args):
    log('Starting worker')
    run_worker_()


def find_worker(sdk, name=WORKER_NAME):
    folder = find_folder(sdk)
    return find_instance(sdk, folder, name)


def create_worker(args):
    create_worker_()


def create_worker_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if instance:
        log('Worker already exists')
        return

    log('Creating worker')
    create_instance(
        sdk,
        name=WORKER_NAME,
        callback=dot,
        **WORKER_CONFIG
    )


def show_worker(args):
    show_worker_()


def show_worker_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if instance:
        print(instance)
    else:
        log('No worker')


def ssh_worker(args):
    ssh_worker_(args.command)


def ssh_worker_(command):
    sdk = get_sdk()
    instance = find_worker(sdk)
    if not instance:
        log('No worker')
        return

    ip = instance_ip(instance)
    client = get_client(ip)
    log('Run: %r' % command)
    ssh_exec(client, command)


def deploy_worker(args):
    deploy_worker_()


def deploy_worker_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if not instance:
        log('No worker')
        return

    ip = instance_ip(instance)
    client = get_client(ip)
    log('Deploying worker')
    deploy_worker__(client)


def remove_worker(args):
    remove_worker_()


def remove_worker_():
    sdk = get_sdk()
    instance = find_worker(sdk)
    if instance:
        log('Removing worker')
        remove_instance(sdk, instance, dot)
    else:
        log('No worker')
