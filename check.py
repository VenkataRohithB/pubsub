import time

from topicExchange import *
exchange = EXCHANGE_NAME
connection=connect_to_rabbitmq()
channel=connection.channel()
declare_exchange(channel=channel,exchange_name=exchange,exchange_type="topic")
while True:
    try:
        time.sleep(5)
        message=str(time.time())
        sender(message=message,message_type="debug",channel=channel,exchange_name=exchange)
    except KeyboardInterrupt:
        print("\nExited")
        break
