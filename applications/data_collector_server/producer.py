import json
import os
import pika

QUEUE_NAME = "weather_events"
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")

def publish_weather_event(weather):
    """
    Publish a weather-collected event to RabbitMQ.
    """
    event = {"event_type": "weather.collected", "weather": weather}
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=json.dumps(event),
        properties=pika.BasicProperties(content_type="application/json", delivery_mode=2))
        connection.close()
        print(f"[Producer] Published weather event for "
              f"{weather['location']}")
        return True
    except pika.exceptions.AMQPError as exc:
        print(f"[Producer] RabbitMQ unavailable: {exc}")
        return False

