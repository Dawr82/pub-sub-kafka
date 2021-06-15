from confluent_kafka import Consumer
from statistics import mean
from time import strftime, localtime, sleep
import mysql.connector


def consumer_loop(consumer, topics):
    consumer.subscribe(topics)
    messages = []
    connection = connect_to_db()
    cursor = connection.cursor()

    while True:
        message = consumer.poll(5)
        if message is None:
            print(f"No message available")
        elif message.error():
            print(f"An error occured: {message.error()}")
            break
        else:
            print(f"[{strftime('%H:%M:%S', localtime())}] Received message: {message.value().decode('utf-8')} ")
            messages.append(float(message.value().decode('utf-8')))

        if len(messages) == 10:
            avg_value = mean(messages)
            messages.clear()
            insert_avg = f"""
                INSERT INTO kafka.temperature(temperature) VALUES({avg_value});
            """
            try:
                cursor.execute(insert_avg)
                connection.commit()
            except mysql.connector.Error as error:
                print(f"Cannot write data to the database! {error}")
            else:
                print(f"Saved average of 10 recent values [{avg_value}] to the database") 

    cursor.close()
    connection.close()
    consumer.close()


def connect_to_db():
    db_config = {
        'user' : 'root',
        'password' : 'dawid',
        'host' : 'mysql',
    }
    while True:
        try:
            connection = mysql.connector.connect(**db_config)
        except mysql.connector.Error:
            sleep(5)
        else:
            break

    return connection


if __name__ == '__main__':

    config = {
        'group.id' : 'temperaturegroup',
        'bootstrap.servers' : 'broker:9092',
        'auto.offset.reset' : 'earliest',
    }

    topics = ['temperature']
    consumer = Consumer(config)
    consumer_loop(consumer, topics)


