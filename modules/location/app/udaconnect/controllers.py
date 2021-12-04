
import json

from app.udaconnect.models import Location
from app.udaconnect.schemas import  LocationSchema
from app.udaconnect.services import  LocationService
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from kafka import KafkaConsumer


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling




@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):  

    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:

        # setup for consumer
        consumer = KafkaConsumer(
        'locations',
        bootstrap_servers=['10.43.188.176:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        max_poll_records=1
        )

        # get data from consumer
        location = {}
        for message in consumer:
            message = message.value.decode('utf-8')
            location = json.loads(message)
            location: Location = LocationService.create(location)
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location

