

README
======

Location Distance Calculator API
-------------------------------

This is a FastAPI application that calculates the distance between multiple locations. It uses a SQLite database to store location data and RabbitMQ for message queuing.

### Features

* Register locations with name, latitude, and longitude
* Calculate distance between multiple locations
* Uses Haversine formula for distance calculation
* Uses Euclidean distance as an alternative calculation method
* Logs events in JSON format using Structlog

### Requirements

* Python 3.8+
* FastAPI
* SQLite
* RabbitMQ
* Pydantic
* Uvicorn

### Installation

1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt`
3. Start the RabbitMQ server
4. Run the application using `uvicorn main:app --host 0.0.0.0 --port 8000`

### API Endpoints

* `POST /register_location`: Register a new location
	+ Request Body: `{"name": "Location Name", "latitude": 36.1289, "longitude": -101.4284}`
	+ Response: `{"id": "location_id"}`
* `POST /calculate_distance`: Calculate distance between multiple locations
	+ Request Body: `{"location_ids": ["location_id1", "location_id2"]}`
	+ Response: `{"total_distance_km": 10.5, "total_distance_ecl": 10.8}`

### Database

The application uses a SQLite database to store location data. The database is created automatically when the application starts.

### RabbitMQ

The application uses RabbitMQ for message queuing. The RabbitMQ server must be running for the application to work.

### Logging

The application logs events in JSON format using Structlog. The logs are output to the console.

### Testing

The application includes tests for the API endpoints. The tests can be run using `pytest`.
