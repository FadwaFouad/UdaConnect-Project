
import logging
import json

from datetime import datetime
from concurrent import futures
from kafka import KafkaConsumer
from google.protobuf.json_format import Parse


import grpc
import urllib3
import location_pb2
import location_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, location, context):
        logging.info("create-location-grpc")

        # use urllib3 to send new location to location service to save it into database
        http = urllib3.PoolManager()
        url = 'http://location-api:5000/api/locations'

        # extract dateTime from timestamp 
        timestamp : Timestamp = location.creation_time
        creation_time = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)

        request_payload = {
            "person_id": location.person_id,
            "longitude": str(location.longitude),
            "latitude": str(location.longitude),
            "creation_time": str(creation_time)
            }

        logging.info(f"request {request_payload}")

        req = http.request('POST', url, body=json.dumps(request_payload), headers={'Content-Type': 'application/json'})
        logging.info(f"request  : {req.data}")

        responce = {
            "person_id": int(location.person_id),
            "longitude": location.longitude,
            "latitude": location.latitude,
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