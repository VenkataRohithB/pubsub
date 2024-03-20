import pika

# Establish connection
cloud_amqp_url="amqps://dzupfdkl:cyEZjbS34eyAm971iIZyF5kgOpEoS3wK@lionfish.rmq.cloudamqp.com/dzupfdkl"
connection = pika.BlockingConnection(pika.URLParameters(cloud_amqp_url))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='my_queue')  # Set TTL of 10 seconds (in milliseconds)

# Publish a message with TTL
channel.basic_publish(exchange='', routing_key='my_queue', body='Hello, RabbitMQ!', properties=pika.BasicProperties(expiration='10000'))  # TTL of 10 seconds (in milliseconds)

# Close connection
connection.close()
