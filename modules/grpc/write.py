import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)


# Update this with desired payload
location = location_pb2.LocationMessage(
    id= 100,
    person_id = 100,
    latitude = '11.5',
    longitude = '10.2', 
    creation_time = '10'
)

 
response = stub.Create(location)
print (response)