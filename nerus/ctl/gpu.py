
import subprocess

from nerus.vast import (
    list_offers,
    preset_offers,
    show_offers,
    create_instance_async,
    wait_label,
    list_instances,
    find_label,
    remove_instance
)
from nerus.log import (
    dot,
    log,
    log_error
)
from nerus.const import (
    SSH_PRIVATE_KEY,
    SSH_CONFIG,

    GPU_LABEL,
    GPU_USER,
    GPU_IMAGE,
    GPU_CONTAINER_PORT
)


#########
#
#   CREATE
#
########


CONFIG = dict(
    image=GPU_IMAGE,
    disk=30
)


def gpu_create(args):
    gpu_create_()


def gpu_create_(label=GPU_LABEL):
    instance = find_label(list_instances(), label)
    if instance:
        log_error('Gpu already exists')
        return

    offers = list(preset_offers(list_offers()))
    show_offers(offers)
    index = int(input('Index:'))
    offer = offers[index]

    log('Creating gpu')
    for key in sorted(CONFIG):
        log('  %s: %s' % (key, CONFIG[key]))

    create_instance_async(offer.id, label=label, **CONFIG)
    wait_label(label, callback=dot)

    config = gpu_config_()
    if not config:
        log_error('No config')
        return
    log('Gpu config: %s', config)


########
#
#   CONFIG
#
########


def gpu_config(args):
    config = gpu_config_()
    if config:
        print(config)


TEMPLATE = '''Host {label}
  Hostname {host}
  Port {port}
  User {user}'''


def gpu_config_(label=GPU_LABEL):
    log('Listing instances')
    instance = find_label(list_instances(), label)
    if not instance:
        log_error('No gpu')
        return

    return TEMPLATE.format(
        label=label,
        host=instance.host,
        port=instance.port,
        user=GPU_USER
    )


###########
#
#   BRIDGE
#
########


def gpu_bridge(args):
    gpu_bridge_()


def gpu_bridge_(label=GPU_LABEL):
    command = [
        'ssh',
        '-i', SSH_PRIVATE_KEY,
        '-F', SSH_CONFIG,
        '-NL', '0.0.0.0:{port}:localhost:{port}'.format(port=GPU_CONTAINER_PORT),
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'StrictHostKeyChecking=no',
        label
    ]
    log('Run: %r', command)
    subprocess.call(command)


##########
#
#    REMOVE
#
##########


def gpu_remove(args):
    gpu_remove_()


def gpu_remove_(label=GPU_LABEL):
    instance = find_label(list_instances(), label)
    if instance:
        log('Removing gpu')
        remove_instance(instance.id)
    else:
        log_error('No gpu')
