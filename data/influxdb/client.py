import os
import time
from typing import List

from base.node import TEACHINGNode
from urllib3.util.retry import Retry
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBClientHandler:

    def __init__(self):
        self._host = os.environ['INFLUXDB_HOST']
        self._port = int(os.environ['INFLUXDB_PORT'])
        self._token = os.environ['INFLUXDB_TOKEN']
        self._org = os.environ['INFLUXDB_ORG']
        self._bucket = os.environ['INFLUXDB_BUCKET']

        self._client = None
        self._write_api = None

        self._build()
    
    @TEACHINGNode(produce=False, consume=True)
    def __call__(self, input_fn):

        for msg in input_fn:
            print(msg)
            if isinstance(msg.timestamp, List):
                for i in range(len(msg.timestamp)):
                    p = Point.from_dict({
                        'measurement': msg.topic,
                        'fields': msg.body[i],
                        'time': msg.timestamp[i]
                    })
                    self._write_api.write(bucket=self._bucket, record=p)
            else:
                p = Point.from_dict({
                    'measurement': msg.topic,
                    'fields': msg.body,
                    'time': msg.timestamp
                })
                self._write_api.write(bucket=self._bucket, record=p)

    def _build(self):
        self._client = InfluxDBClient(
            url=f'http://{self._host}:{self._port}', 
            token=self._token, 
            org=self._org,
            retries=Retry(10, backoff_factor=2.)
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
