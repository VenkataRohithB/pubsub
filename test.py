import pika
import ssl
from urllib.parse import quote_plus

# RabbitMQ connection parameters
rabbitmq_host = 'k1vs3d.stackhero-network.com'
rabbitmq_port = 5671
rabbitmq_user = 'admin'
rabbitmq_password = 'GDoRs1EMNSvRTlIdRQJzxWEadQ22e0MT'  # Replace 'yourPassword' with the actual password
rabbitmq_vhost = '/'  # Default virtual host

# AMQP URI with credentials (password is URL encoded)
amqp_uri = f'amqps://{quote_plus(rabbitmq_user)}:{quote_plus(rabbitmq_password)}@{rabbitmq_host}:{rabbitmq_port}/{rabbitmq_vhost}'

# SSL/TLS context setup
context = ssl.create_default_context(cafile="isrgrootx1.pem")

# Establish connection to RabbitMQ
parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    virtual_host=rabbitmq_vhost,
    credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password),
    ssl_options=pika.SSLOptions(context)
)

connection = pika.BlockingConnection(parameters)

# Open a channel
channel = connection.channel()

# Example: Declare a queue
queue_name = 'my_queue'
channel.queue_declare(queue=queue_name)

# Example: Publish a message to the queue
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='', routing_key=queue_name, body=message)

print(f" [x] Sent '{message}'")

# Close the connection
connection.close()
