import pika

EXCHANGE_NAME = 'test'

# Establishing connection to RabbitMQ server
cloud_amqp_url = 'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl'
connection_parameters = pika.URLParameters(cloud_amqp_url)
connection = pika.BlockingConnection(connection_parameters)


def connect_to_rabbitmq():
    """Establishes a connection to RabbitMQ server."""
    try:
        connection = pika.BlockingConnection(connection_parameters)
        print("Successfully connected to RabbitMQ!")
        return connection
    except pika.exceptions.ConnectionClosed:
        print("Connection failed!")
        return None


def close_connection(connection):
    """Closes the connection to RabbitMQ server."""
    if connection:
        connection.close()


def declare_exchange(channel, exchange_name, exchange_type='topic'):
    """Declares an exchange with optional exchange type."""
    try:
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        print(f"Exchange '{exchange_name}' declared successfully.")
    except Exception as e:
        print(f"Error declaring exchange '{exchange_name}':", e)


def sender(message, message_type, channel, exchange_name):
    """Sends a message to the exchange with the appropriate routing key, marking it as persistent."""
    try:
        routing_key = f"{message_type}.{message}"
        properties = pika.BasicProperties(delivery_mode=2)  # Set delivery mode to persistent
        channel.confirm_delivery()
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=message, properties=properties,
                              mandatory=True)
        print(f" [x] Sent '{message}' with type '{message_type}' to exchange '{exchange_name}'.")
    except pika.exceptions.UnroutableError as e:
        channel.exchange_declare(exchange=f"dlx_{message_type}", exchange_type="fanout")
        channel.basic_publish(exchange=f"dlx_{message_type}", routing_key=f"dlx_{message_type}", body=message,
                              properties=pika.BasicProperties(delivery_mode=2))
        queue_name=f"dlx_{message_type}"
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=f"dlx_{message_type}", queue=queue_name, routing_key=queue_name)
        print(f"Receiver OFFLINE... Sent Message to DLX ")


    except Exception as e:
        print(f"Error sending message to exchange '{exchange_name}':", e)


def dlx_receiver(message_type,channel):
    try:
        def callback(ch, method, properties, body):
            print(f"[x] Received '{body.decode()}'  from DLX ")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Consume messages until the DLX queue is empty

        while True:
            method_frame, header_frame, body = channel.basic_get(queue=f"dlx_{message_type}", auto_ack=False)
            if method_frame:
                callback(channel, method_frame, None, body)
            else:
                break  # No more messages in the DLX queue, exit the loop

        print("DLX queue is empty or the condition is met.")
    except Exception as e:
        print("Error setting up the dlx_receiver:", e)


def receiver(message_type, channel):
    """Declares a durable queue, binds it to the exchange with the specified binding key, and starts consuming messages."""
    dlx_receiver(message_type,channel)
    try:
        # Declare a durable queue (not exclusive)
        result = channel.queue_declare(queue='', exclusive=True,durable=True)
        queue_name = result.method.queue

        # Bind the queue to the exchange with the routing key pattern
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=f"{message_type}.#")

        # Callback function for receiving messages
        def callback(ch, method, properties, body):
            print(f" [x] Received '{body.decode()}' with type '{method.routing_key}'")

            # Process the message here
            # Once processing is complete, acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback,
                              auto_ack=False)  # Manually acknowledge messages
        print(f' [*] Waiting for messages : {message_type}. To exit, press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print("Error setting up receiver:", e)


def main():
    connection = connect_to_rabbitmq()
    if not connection:
        return
    try:
        channel = connection.channel()

        # Declare exchanges and queues
        declare_exchange(channel, EXCHANGE_NAME)
        # sender("Message", "debug", channel, EXCHANGE_NAME)
        receiver("debug", channel)
        # receiver("agv", channel)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        close_connection(connection)


exit_command = False
def test_supervisor():
    while True:
        continue

def main(command: str):
    while True:
        command= input("Enter a command - supervisor, exit:  ")
        if command == "supervisor":
            test_supervisor()
        if command == "exit":
            break
        continue
    return True



if __name__ == '__main__':
    main()
