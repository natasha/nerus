
from redis import Redis
from rq import Queue, Worker

from .const import (
    QUEUE_HOST,
    QUEUE_PORT,
    QUEUE_PASSWORD
)


def get_queue(name, host=QUEUE_HOST, port=QUEUE_PORT, password=QUEUE_PASSWORD):
    connection = Redis(
        host=host,
        port=port,
        password=password
    )
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
