
from redis import Redis
from rq import Queue, Worker, Connection
from rq.cli.helpers import show_both as show_

from .const import (
    QUEUE_HOST,
    QUEUE_PORT,
    QUEUE_PASSWORD
)


def get_connection(host=QUEUE_HOST, port=QUEUE_PORT, password=QUEUE_PASSWORD):
    return Redis(
        host=host,
        port=port,
        password=password
    )


def get_queue(name, connection):
    return Queue(name, connection=connection)


def work_on(queue):
    worker = Worker([queue], connection=queue.connection)
    worker.work()


def enqueue(queue, function, *args):
    queue.enqueue_call(
        func=function,
        args=args,
        timeout=-1,
        ttl=-1
    )


def show(connection):
    with Connection(connection):
        show_(
            queues=None,  # show all
            raw=False,
            by_queue=False,
            queue_class=Queue,
            worker_class=Worker
        )
