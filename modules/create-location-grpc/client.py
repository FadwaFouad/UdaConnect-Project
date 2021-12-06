import logging
import json

from google.protobuf.json_format import MessageToJson
from google.protobuf.timestamp_pb2 import Timestamp
from kafka import KafkaProducer

import grpc
import location_pb2
import location_pb2_grpc
import time

def run():
    logging.getLogger("run")
    with grpc.insecure_channel('location-grpc:50051') as channel:
        stub = location_pb2_grpc.LocationServiceStub(channel)
        print("-------------- Client --------------")

        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        timestamp = Timestamp(seconds=seconds, nanos=nanos)

        location = location_pb2.LocationMessage(
            person_id = 1,
            latitude =  99.0 ,
            longitude =  44.5, 
            creation_time = timestamp
        )

        #send payload to kafka producer
        KAFKA_SERVER = 'kafka-service:9092'
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        kafka_data = MessageToJson(location).encode()
        producer.send("locations", kafka_data)
        producer.flush()

        response = stub.Create(location)
        logging.info("responces: "+ str(response))
      

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
