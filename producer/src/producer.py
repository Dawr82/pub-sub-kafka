from confluent_kafka import Producer
from time import sleep
from random import uniform


def delivery_message(err, msg):
    if err is not None:
        print(f"An error occured! {err}")
    else:
        print(f"Message with value {msg.value()} sent to topic {msg.topic()} on partition {msg.partition()}")


if __name__ == '__main__':

    config = {
        'bootstrap.servers' : 'broker:9092',
    }
    topic = "temperature"

    producer = Producer(config)

    while True:
        producer.poll(0)
        producer.produce(topic, str(round(uniform(10, 30), 2)), on_delivery=delivery_message)
        sleep(uniform(1, 2))

    producer.flush()     

