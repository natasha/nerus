
import paramiko

from .const import (
    SSH_USER,
    SSH_PRIVATE_KEY
)


def get_client(host, user=SSH_USER, key=SSH_PRIVATE_KEY):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=host,
        username=user,
        key_filename=key
    )
    return client


def exec(client, command):
    # https://stackoverflow.com/questions/3823862/paramiko-combine-stdout-and-stderr
    transport = client.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    file = channel.makefile()
    channel.exec_command(command)
    for line in file:
        print(line, end='', flush=True)


def upload(client, source, target):
    connection = client.open_sftp()
    connection.put(source, target)
    connection.close()


def download(client, source, target):
    connection = client.open_sftp()
    connection.get(source, target)
    connection.close()
