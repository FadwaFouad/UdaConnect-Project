import logging
from google.protobuf.timestamp_pb2 import Timestamp
import grpc
import location_pb2
import location_pb2_grpc
import time

def run():
    logging.getLogger("run")
    with grpc.insecure_channel('localhost:30100') as channel:
        stub = location_pb2_grpc.LocationServiceStub(channel)
        logging.getLogger("create-location-grpc")
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
        response = stub.Create(location)
        print(response)
        logging.info("responces: "+ str(response))
      

if __name__ == '__main__':
    logging.basicConfig()
    run()
