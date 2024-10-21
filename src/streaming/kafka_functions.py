from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import logging
import time
import pandas as pd
from model_consumer.model_predict import process_and_predict
from database.db_operations import creating_engine

engine = creating_engine()

df = pd.read_json("../df/happiness_dfset_cleaned.json")

def create_kafka_producer():
    return KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )

def create_kafka_consumer():
    return KafkaConsumer(
        'workshop003_streaming_topic',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092']
    )

def send_in_batches(producer, df, batch_size=5):
    """
    Send df to Kafka in batches.
    
    Parameters:
        producer (KafkaProducer): The Kafka producer instance.
        df (pd.dfFrame): The df to be sent.
        batch_size (int): The size of each batch.
    """
    df = pd.read_json(df)
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size].to_dict(orient='records')
        producer.send("workshop003_streaming_topic", value=batch)
        logging.info(f"Batch sent: {batch}")
        time.sleep(4)  

def kafka_producer(df):
    producer = create_kafka_producer()
    try:
        send_in_batches(producer, df)
        logging.info("Messages to fact table sent")

        return "df sent to Kafka topic"
    except Exception as e:
        logging.error(f"Error creating producer: {e}")
        return None

def kafka_consumer():
    consumer = create_kafka_consumer()
    try:
        for message in consumer:
            mensaje = message.value
        print(f"Mensaje recibido: {mensaje}")

        prediccion, datos_procesados = process_and_predict(mensaje)

        print(f"Predicción: {prediccion}")

        datos_procesados['prediccion'] = prediccion

        datos_procesados.to_sql('tabla_resultados', engine, if_exists='append', index=False)
    except Exception as e:
        logging.error(f"Error consuming messages: {e}")

if __name__ == "__main__":
    kafka_producer() 
    kafka_consumer()