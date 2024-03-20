import time
import pika

cloud_amp_url = 'amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl'
connection_parameters = pika.URLParameters(cloud_amp_url)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

MESSAGE = "Message For Testing "
QUEUE_NAME = "demo"
iters=50
total_time_taken = 0

for i in range(iters):
    # Sender Code
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    start = time.time()
    channel.basic_publish(routing_key=QUEUE_NAME, exchange="", body=MESSAGE)
    publish_lapse = time.time()
    print(f"{MESSAGE} published and took {(publish_lapse - start) * 1000} ms")
    print("")

    # Receiver Code
    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if method_frame:
        print(f"[X] message received {body.decode()}")
        print("")
        receive_lapse = time.time()
        print(f"{(receive_lapse - publish_lapse) * 1000} ms")
        print("")
        channel.basic_publish(routing_key=QUEUE_NAME, exchange="", body=MESSAGE + " RECEIVED FROM THE CONSUMER")
    else:
        print("Message Not Received ")

    # Sender check
    method, head, message = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if method:
        print(f"{message.decode()} gotcha...;)")
        print("")
        end = time.time()
        print(f"{(end - receive_lapse) * 1000} ms")
        print("")
        total_time_taken += (end - start)
    print("")

print(f"Average total time taken for sending and receiving {iters} messages: {(total_time_taken / iters) * 1000} ms")
