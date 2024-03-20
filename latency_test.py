import pika
import time

cloud_amqp_url = 'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl'

def send_message(channel, queue_name, message):
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)

def receive_message(channel, queue_name):
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if method_frame:
        return body.decode('utf-8')
    else:
        return None

def send_media_reference(channel, queue_name, media_reference):
    with open(f"test_files/{media_reference}", 'rb') as file:
        file_content = file.read()

    channel.basic_publish(
        exchange='',
        routing_key='media_queue',
        body=file_content,
        properties=pika.BasicProperties(headers={'file_type': os.path.splitext(media_reference)[1]},
                                        delivery_mode=2)
    )

def receive_media_reference(channel,queue_name):
        method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
        file_name = f"received81"
        with open(f"received_files/{file_name}", 'wb') as file:
            file.write(body)
        print(f"Received file '{file_name}' from sender")
        return "hi"
def measure_latency_messages():
    connection = pika.BlockingConnection(pika.URLParameters(cloud_amqp_url))
    channel = connection.channel()
    queue_name = 'test_queue'

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Send a message
    send_message(channel, queue_name, "Test message")
    start_time = time.time()

    # Receive the message
    received_message = receive_message(channel, queue_name)
    end_time = time.time()

    if received_message:
        latency = (end_time - start_time) * 1000  # in milliseconds
        print(f"Latency: {latency:.2f} ms {received_message} ")
    else:
        print("No message received")
    connection.close()
def measure_latency_media():
    connection = pika.BlockingConnection(pika.URLParameters(cloud_amqp_url))
    channel = connection.channel()
    queue_name = 'media_queue'

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Send a reference to the media file
    media_reference = "2023-09-25_17:17:33@frontviewcamera.mp4"  # Example reference
    send_media_reference(channel, queue_name, media_reference)
    start_time = time.time()

    # Receive the media reference
    received_reference = receive_media_reference(channel, queue_name)
    end_time = time.time()

    if received_reference:
        latency = (end_time - start_time) * 1000  # in milliseconds
        print(f"Latency: {latency:.2f} ms")
    else:
        print("No media reference received")
    connection.close()

if __name__ == "__main__":
    measure_latency_messages()
    # measure_latency_media()
