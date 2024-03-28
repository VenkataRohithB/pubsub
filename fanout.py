import json
import os
import pika

cloud_amqp_url = os.environ.get('CLOUDAMQP_URL',
                                'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl')
connection_parameters = pika.URLParameters(cloud_amqp_url)


def on_message_received(channel, method, properties, body):
    print(f"Received message: {body.decode()}")
    # Send acknowledgment
    channel.basic_ack(delivery_tag=method.delivery_tag)


def receive():
    try:
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        channel.exchange_declare(exchange='messages', exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='messages', queue=queue_name, routing_key='')

        channel.basic_consume(queue=queue_name, on_message_callback=on_message_received, auto_ack=False)

        print("Started")
        channel.start_consuming()
    except pika.exceptions.ConnectionClosed:
        print("Connection closed, reconnecting...")
        receive()


def send_messages(msg: dict):
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # Declare the exchange (fanout for broadcasting)
    channel.exchange_declare(exchange='messages', exchange_type='fanout')

    # Message to send
    message = json.dumps(msg)

    # Publish the message to the exchange
    channel.basic_publish(exchange='messages', routing_key='', body=message.encode())
    print(f"Sent message: {message}")

    # Close the connection
    connection.close()

a =input()
if a == "1":
    msg = {"hello": 123}
    send_messages(msg)
else:
    receive()