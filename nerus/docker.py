

import re
import subprocess

from .utils import Record


class DockerError(Exception):
    @classmethod
    def from_subprocess(cls, error):
        message = 'stderr: {stderr}, stdout: {stdout}'.format(
            stderr=error.stderr.decode('utf8'),
            stdout=error.stdout.decode('utf8')
        )
        return cls(message)


class Container(Record):
    __attributes__ = ['name', 'port']

    def __init__(self, name, port):
        self.name = name
        self.port = port


#############
#
#   LIST
#
#########


def parse_port(string):
    # 0.0.0.0:8080->80/tcp
    match = re.search(r'(\d+)->\d+', string)
    if match:
        return int(match.group(1))


def list_containers():
    try:
        output = subprocess.check_output([
            'docker', 'ps',
            '--format', '{{.Names}}\t{{.Ports}}'
        ])
    except subprocess.CalledProcessError as error:
        raise DockerError.from_subprocess(error)
    else:
        lines = output.decode('utf8').splitlines()
        for line in lines:
            name, port = line.split('\t', 1)
            port = parse_port(port)
            yield Container(name, port)


###########
#
#   NAME
#
##########


def list_names():
    for record in list_containers():
        yield record.name


def generate_name(prefix, start=1, delta=1000):
    stop = start + delta
    names = set(list_names())
    for index in range(start, stop):
        name = '%s_%d' % (prefix, index)
        if name not in names:
            return name
    raise DockerError('no free name, %s_%d..%d' % (prefix, start, stop))


def container_exists(name):
    return name in list_names()


###########
#
#  PORT
#
##########


def list_ports():
    for record in list_containers():
        if record.port:
            yield record.port


def generate_port(start, delta=1000):
    stop = start + delta
    ports = set(list_ports())
    for port in range(start, stop):
        if port not in ports:
            return port
    raise DockerError('no free port, %d..%d' % (start, stop))


#########
#
#   CREATE
#
#########


def start_container(image, name, container_port, port):
    if container_exists(name):
        return

    command = [
        'docker', 'run', '-d',
        '-p', '%d:%d' % (port, container_port),
        '--name', name,
        image
    ]
    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as error:
        remove_container(name)
        raise DockerError.from_subprocess(error)


def remove_container(name):
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
        raise DockerError.from_subprocess(error)
