import os

from .communication.pubsub import RabbitMQProducer, RabbitMQConsumer


class TEACHINGNode(object):

    def __init__(self, produce, consume):
        self._id = os.environ['SERVICE_NAME']
        self._mq_params = {
            'user': os.environ['RABBITMQ_USER'],
            'password': os.environ['RABBITMQ_PASSWORD'],
            'host': os.environ['RABBITMQ_HOST'],
            'port': os.environ['RABBITMQ_PORT']
        }

        self._produce = produce
        self._producer = None

        self._consume = consume
        if self._consume:
            it = os.environ['TOPICS']
            self._topics = it.split(',') if ',' in it else [it]
        self._consumer = None

        self._build()
    

    def _build(self):
        print("Building the TEACHING Node...")

        if self._produce:
            self._producer = RabbitMQProducer(self._mq_params)

        if self._consume:
            self._consumer = RabbitMQConsumer(self._mq_params, self._topics)

        print("Done!")


    def __call__(self, service_fn):
        
        def service_pipeline(*args):
            obj = args[0]
            if self._consume and not self._produce:
                service_fn(obj, self._consumer())


            if not self._consume and self._produce:
                self._producer(service_fn(obj))


            if self._consume and self._produce:
                self._producer(service_fn(obj, self._consumer()))
        
        return service_pipeline
