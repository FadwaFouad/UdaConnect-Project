
import logging

from kafka import KafkaConsumer
from google.protobuf.json_format import Parse

import grpc
import location_pb2_grpc
import location_pb2


def run():
    logging.info("run consumer")

    # setup for consumer
    consumer = KafkaConsumer(
    'locations',
    bootstrap_servers=['kafka-service:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
    )

    # get data from consumer
    location = {}
    while (True):
        message = message.value.decode('utf-8')
        location=location_pb2.LocationMessage()
        Parse(str(message), location)

        logging.info(location)
        with grpc.insecure_channel('location-grpc:50051') as channel:
            stub = location_pb2_grpc.LocationServiceStub(channel)
            response = stub.Create(location)
            logging.info(response)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("consumer")
    run()