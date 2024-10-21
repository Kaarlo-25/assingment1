import pika
import pymongo
import json

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/") # In the assignement it is necessary to specify the user (root), and the password (password)
db = mongo_client["test"]
collection = db["messages"]

# Connect to RabbitMQ
rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = rabbitmq_conn.channel()
channel.queue_declare(queue='message_queue')

# Callback function to handle messages
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received {message}")
    
    # Save the message to MongoDB
    collection.insert_one(message)
    print(" [x] Message stored in MongoDB:", message)

# Consume messages from RabbitMQ
channel.basic_consume(queue='message_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
