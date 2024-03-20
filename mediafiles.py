import os
import sys
from datetime import datetime
import pika

def send_media(file_path, sender_id):
    try:
        if os.path.exists(f"test_files/{file_path}"):
            url = os.environ.get('CLOUDAMQP_URL',
                                 'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl')
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.queue_declare(queue='media_queue')

            sender_id = sender_id

            with open(f"test_files/{file_path}", 'rb') as file:
                file_content = file.read()

            channel.basic_publish(
                exchange='',
                routing_key='media_queue',
                body=file_content,
                properties=pika.BasicProperties(headers={'sender_id': sender_id, 'file_type': os.path.splitext(file_path)[1]},delivery_mode=2)
            )

            print(f"Sent file '{file_path}' with sender ID {sender_id}")
        else:
            print("File not found.")
    except Exception as e:
        print(f"Error occurred while sending file: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def receive_media():
    try:
        url = os.environ.get('CLOUDAMQP_URL',
                             'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='media_queue')

        def callback(ch, method, properties, body):
            sender_id = properties.headers.get('sender_id')
            file_type = properties.headers.get('file_type')
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"received_file_{sender_id}_{timestamp}_{file_type}"
            with open(f"received_files/{file_name}", 'wb') as file:
                file.write(body)
            print(f"Received file '{file_name}' from sender {sender_id}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue='media_queue', on_message_callback=callback, auto_ack=False)

        print('Waiting for media files...')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
    except Exception as e:
        print(f"Error occurred while receiving files: {e}")
    finally:
        connection.close()

send_media("file.csv",54)
# receive_media()