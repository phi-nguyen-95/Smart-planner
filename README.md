# Smart Planner

Smart Planner is a weather-based outdoor activity planning web application built with Python and Flask.
The application collects live weather data, stores weather observations, analyzes outdoor conditions and provides an activity score and weather trend analysis.

## Live Application

https://smart-planner-phi-b58e7a19b159.herokuapp.com

## Features

- Search weather by location
- Fetch live weather data from an external REST API
- Store weather observations in a SQL database
- Calculate an outdoor activity score and rating
- Analyze changes between recent weather observations
- Display weather history
- REST communication between application services
- RabbitMQ event collaboration
- Unit, mock-object, and integration testing
- `/health` and `/metrics` monitoring endpoints
- GitHub Actions Continuous Integration
- Automatic deployment to Heroku

## Architecture
External Weather API
        |
        v
Data Collector
        |
        v
Weather Database
        |
        +--------> Basic Web Server
        |               |
        |               | REST
        |               v
        |         Data Analyzer
        |
        +--------> RabbitMQ Producer
                         |
                         v
                  weather_events
                         |
                         v
                      Consumer

The REST connection provides synchronous communication between the web server and analyzer.

RabbitMQ provides asynchorous event collaboration between the weather producer and consumer.

## Project Structure

applications/
|-- basic server/
|-- data_collector_server/
|-- data_analyzer_server/

components/
|-- database/

tests/
|-- unit_test/
|-- mock_object_test/
|-- integration_test

## Technologies:
- Python
- Flask
- SQLAlchemy
- SQLite
- REST APIs
- RabbitMQ/ Pika
- Gunicorn
- GitHub Actions
- Heroku

## Run locally

Clone the repository:
git clone https://github.com/phi-nguyen-95/Smart-planner.git
cd Smart-planner

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run Smart Planner:
PORT=5002 bash start.sh

Open:
http://127.0.0.1:5002

## Run Tests

Run the complete automated test suite:
./run_tests.sh

The test suite uses a temporary isolated database so test data does not modify the normal application database.

## RabbitMQ Event Messaging

Start RabbitMQ:
brew services start rabbitmq

Start the consumer:
python3 -m applications.data_analyzer_server.consumer

When weather data is collected, the producer publishes a `weather.collected` event to the `weather_events` queue.

Producer -> RabbitMQ -> Consumer -> Weather Analysis

RabbitMQ messaging is currently demonstrated locally.

## Monitoring:

Health endpoint:
/health

Metrics endpoint:
/metrics

## Continuous Integration and Deployment

GitHub Actions automatically run the test suite when code is pushed.

git push -> GitHub Actions -> Automated Tests -> Tests Pass -> Heroku Automatic Deployment

The production application is automatically deployed fro the `main` branch after GitHub checks pass.

## Data Analysis

Smart Planner analyzes:

- Temperature
- Humidity
- Precipitation
- Wind Speed

It generates an outdoor activity score and rating.

The application also compares recent weather records for the same location to determine weather trend.

## Testing

The project includes:

- Unit tests: verify individual analyis functions
- Mock-object tests: isolate the weather API and RabbitMQ
- Integration tests: verify communication between application components

## Known Limitation:

Smart Planner implements data persistence using SQLAlchemy and SQLite.

The Heroku deployment also uses SQLites; however, Heroku's filesystem is ephemeral, so stored weather history may be reset when the application dyno restarts.

## Author

Phi Nguyen

Software Engineering Final Project  
