import pika
import json

# Connect to RabbitMQ
rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = rabbitmq_conn.channel()
channel.queue_declare(queue='message_queue')

# Define the message
message = {"text": "Hello, this is a test message from the publisher!"}

# Publish the message to the queue
channel.basic_publish(exchange='', routing_key='message_queue', body=json.dumps(message))

print(" [x] Sent message:", message)

# Close the RabbitMQ connection
rabbitmq_conn.close()
