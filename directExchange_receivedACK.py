import pika
import uuid
import json
import os

# CloudAMQP credentials
cloud_amqp_url = os.environ.get('CLOUDAMQP_URL',
                                'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl')
connection_parameters = pika.URLParameters(cloud_amqp_url)


def send_message(message):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # Declare the exchange for sending messages to the receiver
    channel.exchange_declare(exchange='messages', exchange_type='direct')

    # Generate a unique message ID
    message_id = str(uuid.uuid4())

    # Prepare message payload (including message ID)
    message_data = {'message': message, 'id': message_id}

    # Send the message to the exchange with a routing key
    channel.basic_publish(exchange='messages',
                          routing_key='receiver_1',
                          body=json.dumps(message_data).encode())
    print("Message Successfully Sent...")
    connection.close()

def send_log_message(log_message):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='log_queue', body=log_message.encode())
    connection.close()

def start_receiver(receiver_id):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue=receiver_id)
    channel.queue_bind(exchange='messages', queue=receiver_id, routing_key=receiver_id)

    def handle_message(ch, method, props, body):
        message_data = json.loads(body.decode())
        message = message_data['message']
        message_id = message_data['id']

        # Process the received message
        print(f"Received message (ID: {message_id}): {message} from sender")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # Send receiver message log to the log queue
        send_log_message(f"Received message (ID: {message_id}): {message} from sender")

    channel.basic_consume(queue=receiver_id, on_message_callback=handle_message,auto_ack=False)

    print(f"Receiver '{receiver_id}' waiting for messages...")
    channel.start_consuming()

def display_logs():
    # Start consuming and displaying logs
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='log_queue')

    def handle_log_message(ch, method, props, body):
        log_message = body.decode()
        print(f"Log: {log_message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue='log_queue', on_message_callback=handle_log_message, auto_ack=False)

    print("Displaying Received Messages...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()


while True:
    user_input = input("Choose an action:\n1. Send Message\n2. Receive Messages\n3. Display Received messages\nEnter a number (or 'q' to quit): ")

    if user_input == '1':
        message = input("Enter message to send: ")
        send_message(message)
    elif user_input == '2':
        receiver_id = 'receiver_1'
        start_receiver(receiver_id)
    elif user_input == '3':
        display_logs()
    elif user_input.lower() == 'q':
        break
    else:
        print("Invalid input. Please choose a valid option.")

print("Exiting...")
