
import logging
import json

from datetime import datetime
from concurrent import futures
from kafka import KafkaProducer

import grpc
import urllib3
import location_pb2
import location_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        logging.info("create-location-grpc")
        # extract dateTime from timestamp 
        timestamp : Timestamp = request.creation_time
        creation_time = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)

        # payload to save in database
        request_payload = {
            "person_id": int(request.person_id),
            "longitude": str(request.longitude),
            "latitude": str(request.latitude),
            "creation_time": str(creation_time)
        }

        #send payload to kafka producer
        KAFKA_SERVER = '10.43.188.176:9092'
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        kafka_data = json.dumps(request_payload).encode()
        producer.send("locations", kafka_data)
        producer.flush()

        # use urllib3 to send new location to location service to save it into database
        http = urllib3.PoolManager()
        url = 'http://10.42.0.136:5000/api/locations'
        req = http.request('POST', url,
                 headers={'Content-Type': 'application/json'})
        logging.info(f"request data : {request_payload}")
        logging.info(f"request  : {req.data}")

        # return responce to client
        responce = {
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": timestamp
        }
        return location_pb2.LocationMessage(**responce)

def serve () :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
    logging.info( 'gRPC server starting on port 50051.')
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("main")
    serve()