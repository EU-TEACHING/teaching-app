import os
from threading import Thread
from typing import Iterator
import pika
from queue import Queue

from .packet import DataPacket

class RabbitMQHandler:

    def __init__(self, params):
        self._config = pika.ConnectionParameters(
            host=params['host'], 
            port=params['port'],
            virtual_host='/',
            credentials=pika.PlainCredentials(params['user'], params['password']),
            connection_attempts=5,
            retry_delay=10,
            socket_timeout=5
        )
        self._connection = pika.BlockingConnection(self._config) 
        self._channel = self._connection.channel()


class RabbitMQProducer(RabbitMQHandler):

    def __call__(self, msg_stream: Iterator[DataPacket]) -> None:
        for msg in msg_stream:
            self._channel.basic_publish(
                exchange='amq.topic', 
                routing_key=msg.topic, 
                body=msg.dumps()
            )


class RabbitMQConsumer(RabbitMQHandler):

    def __init__(self, params, topics):
        super(RabbitMQConsumer, self).__init__(params)
        self._queue = f"{os.environ['SERVICE_NAME']}.queue"
        self._channel.queue_declare(queue=self._queue, exclusive=True, auto_delete=True)

        for t in topics: 
            self._channel.queue_bind(exchange=f'amq.topic', queue=self._queue, routing_key=t)

        self._data = Queue()

    def __call__(self):
        self._channel.basic_consume(
            self._queue, 
            on_message_callback=lambda ch, method, properties, body: self._data.put(DataPacket.from_json(body)),
            auto_ack=True
        )
        consumption = Thread(target=self._channel.start_consuming)
        consumption.start()
        while True:
            yield self._data.get()
