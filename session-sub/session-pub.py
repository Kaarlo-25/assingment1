import datetime
import os
import random
import time
import pika
import json

QUEUE_NAME = 'session_queue'
NUM_SESSIONS = int(os.getenv('NUM_SESSIONS'))
DELAY = int(os.getenv('SESSION_DELAY'))
AMQP_SERVER = os.getenv('AMQP_SERVER')
user_ids_used = []

# FUNCTIONS
def generate_id():
    session_id = f"session_{datetime.now().strftime('%H:%M:%S')}" 
    user_id = random.randint(1, 9999)
    while user_id in user_ids_used:
        user_id = random.randint(1, 9999)
    user_ids_used.append(user_id)
    return session_id, user_id

def publish_message(channel, message):
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message))
    print(f"Published: {message}")

def simulate_session(channel, session_id, user_id):
    # Start session event
    start_time = datetime.now().isoformat()
    start_event = {
        'event_type': 'session_start',
        'session_id': session_id,
        'user_id': user_id,
        'start_time': start_time
    }
    publish_message(channel, start_event)
    
    session_duration = random.randint(1, DELAY)
    time.sleep(session_duration)
    
    # End session event
    end_time = datetime.now().isoformat()
    end_event = {
        'event_type': 'session_end',
        'session_id': session_id,
        'end_time': end_time
    }
    publish_message(channel, end_event)

credentials = pika.PlainCredentials('kaarlo', 'password1')
rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_SERVER, credentials=credentials))
channel = rabbitmq_conn.channel()

channel.queue_declare(queue=QUEUE_NAME, durable = False)

for _ in range(NUM_SESSIONS):
    session_id, user_id = generate_id()
    simulate_session(channel, session_id, user_id)

rabbitmq_conn.close()
