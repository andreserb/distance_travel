from fastapi import FastAPI, HTTPException
import uuid
from typing import Dict
from models import LocationModel, DistanceRequest
from database import Database
from utils import haversine_distance, calculate_euclidean_distance
import uvicorn
import pika
import json
import structlog
from structlog import get_logger

# Initialize the logger
logger = get_logger()
# Configure structlog to output logs in a JSON format
# Output logs in a JSON format on console
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True)
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory()
)

# Initialize FastAPI application
app = FastAPI()

# RabbitMQ connection settings
rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_queue_inbound = 'inbound'
rabbitmq_queue_outbound = 'outbound'

@app.post("/register_location")
def register_location(location: LocationModel):
    # Generate a unique ID for each location
    loc_id = str(uuid.uuid4())
    # Save location to the database
    loc = Database(loc_id, location.name, location.latitude, location.longitude)
    loc.save_location()
    logger.info("Location registered", location_id=loc_id, name=location.name, 
                latitude=location.latitude, longitude=location.longitude)
    return {"id": loc_id}

def calculate_distance_wrapper(location_ids):
    total_distance = 0.0
    locations = []

    # Retrieve locations from the database
    for loc_id in location_ids:
        location = Database.get_location(loc_id)
        if not location:
            raise HTTPException(status_code=404, detail=f"Location with ID {loc_id} not found")
        locations.append(location)

    # Calculate cumulative distance
    for i in range(len(locations) - 1):
        loc1, loc2 = locations[i], locations[i + 1]
        total_distance += haversine_distance(loc1["latitude"], loc1["longitude"], loc2["latitude"], loc2["longitude"])
        total_distance_ecl = calculate_euclidean_distance(loc1["latitude"], loc1["longitude"], loc2["latitude"], loc2["longitude"])
    
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()

    # Publish the result to the outbound queue
    result = {"total_distance_km": total_distance, "total_distance_ecl": total_distance_ecl}
    logger.info("Publishing result to outbound queue", result=result)
    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_queue_outbound,
                          body=json.dumps(result))

    connection.close()
    return result
@app.post("/calculate_distance")
def calculate_distance(request: DistanceRequest):
    location_ids = request.location_ids
    if len(location_ids) < 2:
        raise HTTPException(status_code=400, detail="At least two locations are required to calculate distance")

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()

    # Publish the location IDs to the inbound queue
    logger.info("Publishing location IDs to inbound queue", location_ids=location_ids)
    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_queue_inbound,
                          body=str(location_ids))
    # Call the wrapper function to calculate the distance
    result = calculate_distance_wrapper(location_ids)
    logger.info("Distance calculated", result=result)
    connection.close()
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)