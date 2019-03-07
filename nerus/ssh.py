
from pssh.clients.native.single import SSHClient

from .const import (
    SSH_USER,
    SSH_PRIVATE_KEY
)


def get_client(host, user=SSH_USER, key=SSH_PRIVATE_KEY):
    return SSHClient(
        host,
        user=user,
        pkey=key
    )


def exec(client, command, sudo=True):
    _, host, stdout, stderr, _ = client.run_command(command, sudo=sudo)
    for line in stdout:
        print(line)
    for line in stderr:
        print('[err] %s' % line)


def cp(client, source, target):
    client.copy_file(source, target)
