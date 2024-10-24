import datetime
import os
import pika
import pymongo
import json

QUEUE_NAME = 'session_queue'
AMQP_SERVER = os.getenv('AMQP_SERVER')
MONGO_SERVER = os.getenv('MONGO_SERVER')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')

# Connect to MongoDB
mongo_client = pymongo.MongoClient(f"mongodb://{MONGO_SERVER}:27017/") # In the assignement it is necessary to specify the user (root), and the password (password)
db = mongo_client[MONGO_DATABASE]
collection = db["sessions"]

# Connect to RabbitMQ
credentials = pika.PlainCredentials('kaarlo', 'password1')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_SERVER, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=False)

sessions_store = {}

# Callback function to handle messages
def callback(body):
    message = json.loads(body)
    session_id = message['session_id']
    event_type = message['event_type']
    
    if event_type == 'session_start':
        # Store session start info
        start_time = message['start_time']
        sessions_store[session_id] = {'start_time': start_time}
        print(f"Session started: {session_id} at {start_time}")
    
    elif event_type == 'session_end':
        # Check if we have the session start info
        if session_id in sessions_store:
            end_time = message['end_time']
            start_time = sessions_store[session_id]['start_time']

            # Calculate session duration
            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            duration = (end_dt - start_dt).total_seconds()

            # Store the session in MongoDB
            session_data = {
                'session_id': session_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration
            }
            collection.insert_one(session_data)

            # Remove the session from sessions_store
            del sessions_store[session_id]
            print(f"Session ended: {session_id} at {end_time}, duration: {duration} seconds")
        else:
            print(f"Received end event for unknown session: {session_id}")

# Consume messages from RabbitMQ
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("Waiting for session messages. To exit, press CTRL+C")
channel.start_consuming()