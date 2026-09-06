import json
import os
import pika
from applications.data_analyzer_server.analyzer import calculate_activity_score, get_activity_rating

QUEUE_NAME = "weather_events"
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")

def process_weather_event(weather):
    """
    Analyze a weather event recieved from RabbitMQ.
    """
    score = calculate_activity_score(weather["temperature"], weather["precipitation"],
            weather["wind_speed"], weather["humidity"])

    rating = get_activity_rating(score)
    print("\n--------------------------------")
    print("Weather event recieved")
    print(f"Location: {weather['location']}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Humidity: {weather['humidity']} %")
    print(f"Precipitation: {weather['precipitation']} mm")
    print(f"Wind Speed: {weather['wind_speed']} km/h")
    print(f"Activity Score: {score}")
    print(f"Rating: {rating}")
    print("--------------------------------\n")

def callback(channel, method, properties, body):
    try:
        event = json.loads(body.decode("utf-8"))
        if event.get("event_type") == "weather.collected":
            process_weather_event(event["weather"])
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as exc:
        print(f"[Consumer] Failed to process maessage: {exc}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("[Consumer] Waiting for weather events.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[Consumer] Stopping...")
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()

    

