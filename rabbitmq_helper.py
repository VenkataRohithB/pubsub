import json

import pika

EXCHANGE_NAME = 'test'

# Establishing connection to RabbitMQ server
cloud_amqp_url = 'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl'


def pubsub_startup():
    try:
        connection_parameters = pika.URLParameters(cloud_amqp_url)
        connection = pika.BlockingConnection(connection_parameters)
        msg_handle = connection.channel()
        return msg_handle
    except pika.exceptions.ConnectionClosed:
        print("Connection failed!")



def pubsub_shutdown(msg_handle):
    if msg_handle:
        print("Connection Closed...")
        msg_handle.close()



def pubsub_publish_message(msg_handle, msg_topic, msg):
    try:
        routing_key = f"{msg_topic}"
        msg_handle.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")
        properties = pika.BasicProperties(delivery_mode=2)
        msg_handle.confirm_delivery()
        msg_handle.basic_publish(exchange=EXCHANGE_NAME, routing_key=routing_key, body=msg, properties=properties, mandatory=True)
        return True

    except pika.exceptions.UnroutableError as e:
        print(f"Receiver OFFLINE... Please Make Sure Receiver is Online...")

    except Exception as e:
        print(f"Error sending message to exchange '{EXCHANGE_NAME}':", e)


def pubsub_retrieve_message(msg_handle, msg_topic):
    try:
        result = msg_handle.queue_declare(queue='', exclusive=True,durable=True)
        queue_name = result.method.queue
        msg_handle.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=f"{msg_topic}.#")
        def callback(ch, method, properties, body):
            msg=(body.decode())
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            print(msg)
        # method_frame, header_frame, body = msg_handle.basic_get(queue=queue_name, auto_ack=False)
        # if method_frame:
            # callback(ch=msg_handle, method=method_frame, properties=None, body=body)

        msg_handle.basic_consume(queue=queue_name, on_message_callback=callback,
                              auto_ack=False)  # Manually acknowledge messages
        print(f' [*] Waiting for messages : {msg_topic}. To exit, press CTRL+C')
        msg_handle.start_consuming()

    except Exception as e:
        print("Error setting up receiver:", e)

msg_handle = pubsub_startup()
a=input("Enter 1-Send, 2-Receive: ")
if a =="1":
    topic=input("Enter topic: ")
    message=input("Enter the message: ")
    publish = pubsub_publish_message(msg_handle=msg_handle,msg_topic=topic, msg=message)
    if publish:
        print(f"Message- {message} sent to topic-{topic} successfully")
    else:
        print("Error occurred in sending message")
elif a=="2":
    topic=input("Enter topic: ")
    pubsub_retrieve_message(msg_handle=msg_handle, msg_topic=topic)