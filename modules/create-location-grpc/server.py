
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
    def Create(self, request, context):
        logging.info("create-location-grpc")

        # setup for consumer
        consumer = KafkaConsumer(
        'locations',
        bootstrap_servers=['kafka-service:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        # request_timeout_ms=30000,
        # max_poll_records=1
        )
        logging.info(f"consumer")


        # get data from consumer
        location = {}
        for message in consumer:
            logging.info(f"message before  : {message}")
            message = message.value.decode('utf-8')
            logging.info(f"message after  : {message}")
            location=location_pb2.LocationMessage()
            Parse(str(message), location)
            #locations.append(location)
            logging.info(f"locations  : {location}")

            logging.info(f"after  : loop")
            # use urllib3 to send new location to location service to save it into database
            http = urllib3.PoolManager()
            url = 'http://location-api:5000/api/locations'
            # for i in range(len(locations)):

            # extract dateTime from timestamp 
            timestamp : Timestamp = location.creation_time
            creation_time = datetime.fromtimestamp(timestamp.seconds + timestamp.nanos/1e9)


            
            logging.info(location.person_id)
            # logging.info(location['person_id'])

            request_payload = {
                "person_id": location.person_id,
                "longitude": str(location.longitude),
                "latitude": str(location.longitude),
                "creation_time": str(creation_time)
                }

            logging.info(f"request {request_payload}")
            logging.info(f"request dumbs  {json.dumps(request_payload)}")

            req = http.request('POST', url, body=json.dumps(request_payload), headers={'Content-Type': 'application/json'})
            logging.info(f"request  : {req.data}")
        logging.info(f" {location} Messages founded ")


            
            

        # request_payload = {
        #     "person_id": int(locations.index(i).person_id),
        #     "longitude":str(locations.index(i).longitude),
        #     "latitude": str(locations.index(i).latitude),
        #     "creation_time": str(creation_time)
        # }



            # # create request data to post in Location Service 
            # request_payload = {
            # "person_id": int(locations[i]['person_id']),
            # "longitude": str(locations[i]['longitude']),
            # "latitude": str(locations[i]['latitude']),
            # "creation_time": str(creation_time)
            # }

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