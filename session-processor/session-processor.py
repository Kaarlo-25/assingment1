from datetime import datetime
import os
import pika
import pymongo
import json

QUEUE_NAME = 'session_queue'
AMQP_SERVER = os.getenv('AMQP_SERVER')
MONGO_SERVER = os.getenv('MONGO_SERVER')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')

mongo_client = pymongo.MongoClient(f"mongodb://root:mypassword@{MONGO_SERVER}:27017/") 
db = mongo_client[MONGO_DATABASE]
collection = db["sessions"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_SERVER))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

sessions_store = {}

def callback(ch, method, properties, body):
    message = json.loads(body)
    session_id = message['session_id']
    event_type = message['event_type']
    
    if event_type == 'session_start':
        start_time = message['start_time']
        sessions_store[session_id] = {'start_time': start_time}
        print(f"Session started: {session_id} at {start_time}")
    
    elif event_type == 'session_end':
        if session_id in sessions_store:
            end_time = message['end_time']
            start_time = sessions_store[session_id]['start_time']

            start_dt = datetime.fromisoformat(start_time)
            end_dt = datetime.fromisoformat(end_time)
            duration = (end_dt - start_dt).total_seconds()

            session_data = {
                'session_id': session_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration
            }
            collection.insert_one(session_data)
            del sessions_store[session_id]
            print(f"Session ended: {session_id} at {end_time}, duration: {duration} seconds")
        else:
            print(f"Received end event for unknown session: {session_id}")

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print("Waiting for session messages. To exit, press CTRL+C")
channel.start_consuming()