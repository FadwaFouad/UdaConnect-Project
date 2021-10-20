
import logging
from datetime import datetime
# import Location
from app.udaconnect.models import Location
from app.udaconnect.services import  LocationService

from concurrent import futures
import grpc
import location_pb2
import location_pb2_grpc
from flask_restx import Namespace
from flask import Flask

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("create-location-grpc")
logging.log(logging.INFO, 'inside grpc ')

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
request_value={}

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):

        request_value = {
            "id": int(request.id),
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": datetime.strptime(request.creation_time,DATE_TIME_FORMAT),
        }
        
        location: Location = LocationService.create(request_value.get_json())
        logger.info(f"Location created : {request_value}")
        return location_pb2.LocationMessage(**request_value)

 
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)
logging.log(logging.INFO, 'gRPC server starting on port 5000.')
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()


