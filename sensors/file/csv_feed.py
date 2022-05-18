import csv
import os
import time

from base.communication.packet import DataPacket
from base.node import TEACHINGNode

class CSVFeed:

    def __init__(self):
        self._path = os.environ['FILE_PATH']
        self._output_topic = os.environ['OUTPUT_TOPIC']
        self._transmit_rate = float(os.environ['TRANSMIT_RATE'])
        self._headers = []
        self._rows = []
        self._build()

    @TEACHINGNode(produce=True, consume=False)
    def __call__(self):
        i = 0
        while True:
            yield DataPacket(topic=self._output_topic, body=dict(zip(self._headers, self._rows[i])))

            i = i + 1 if i < len(self._rows) - 1 else 0
            time.sleep(self._transmit_rate)

    def _build(self):
        print("Building the CSV file reader...")
        with open(self._path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self._headers = next(csv_reader)
            for row in csv_reader:
                self._rows.append([float(x) for x in row])
        print("Done!")