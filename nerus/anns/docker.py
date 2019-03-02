
import sys
import subprocess
from time import sleep

import requests

from nerus.log import log


def list_containers():
    output = subprocess.check_output([
        'docker', 'ps',
        '--format', '{{.Names}}'
    ])
    return output.decode('utf8').splitlines()


def container_exists(name):
    return name in list_containers()


def start_container(image, name, container_port, port):
    if container_exists(name):
        log('Running %s', name)
        return

    command = [
        'docker', 'run', '-d',
        '-p', '%d:%d' % (port, container_port),
        '--name', name,
        image
    ]
    log('Start %s: %r', name, command)
    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        sys.stderr.buffer.write(error.stderr)
        sys.stderr.buffer.write(error.stdout)
        stop_container(name)
        raise


def stop_container(name):
    if not container_exists(name):
        return

    command = [
        'docker', 'rm',
        '--force', name  # kill + rm
    ]
    try:
        subprocess.run(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        sys.stderr.buffer.write(error.stderr)
        sys.stderr.buffer.write(error.stdout)
        raise


PUTIN = ['Путин']


def warmup_container(call, retries=10, delay=2):
    for retry in range(retries):
        try:
            list(call(PUTIN))
        except (requests.ConnectionError, requests.ReadTimeout):
            log('Warmup call %d / %d', retry, retries)
            sleep(delay)
        else:
            log('Success!')
            return
    raise RuntimeError('Warmup failed')
