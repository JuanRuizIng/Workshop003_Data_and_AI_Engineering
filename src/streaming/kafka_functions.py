from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import logging
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.model_consumer.model_predict import process_and_predict
from src.database.db_operations import creating_engine
from src.feature_selection.df_cleaned import clean_and_concat_csv_data

# Configurar logging
logging.basicConfig(level=logging.INFO)

kafka_topic = 'workshop003_streaming_topic'
engine = creating_engine()

def create_kafka_producer():
    """ Create a Kafka producer
    Parameters:
    None
    
    Returns:
    producer (kafka.producer.kafka.KafkaProducer): Kafka producer.
    """


    return KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )

def create_kafka_consumer():
    """ Create a Kafka consumer
    Parameters:
    None

    Returns:
    consumer (kafka.consumer.group.KafkaConsumer): Kafka consumer.
    """
    return KafkaConsumer(
        kafka_topic,
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092']
    )

def kafka_producer():
    """ Send data to a Kafka topic
    Parameters:
    None

    Returns:
    str: Message sent to Kafka topic.
    """

    producer = create_kafka_producer()
    try:
        data = clean_and_concat_csv_data()
        n_samples = int(len(data) * 0.30)
        # Se usa el random_state para obtener los mismos resultados
        df = data.sample(n=n_samples, random_state=42)
        for _, row in df.iterrows():
            message = {
                "country": row["country"],
                "happiness_rank": row["happiness_rank"],
                "happiness_score": row["happiness_score"],
                "gdp_per_capita": row["gdp_per_capita"],
                "family": row["family"],
                "health": row["health"],
                "freedom": row["freedom"],
                "trust_government_corruption": row["trust_government_corruption"],
                "generosity": row["generosity"],
                "year": row["year"]
            }
            producer.send(kafka_topic, value=message)
            logging.info("Message sent to Kafka topic")
        return "df sent to Kafka topic"
    except Exception as e:
        logging.error(f"Error creating producer: {e}")
        return None

def kafka_consumer():
    """ Consume data from a Kafka topic
    Parameters:
    None

    Returns:
    None
    """

    consumer = create_kafka_consumer()
    for message in consumer:
        mensaje = message.value
        logging.info(f"Mensaje recibido: {mensaje}")
        df1 = pd.DataFrame([mensaje])
        try:
            columns_to_drop = ['happiness_score', 'country']
            df_temporal = df1.drop(columns=[col for col in columns_to_drop if col in df1.columns])
            prediccion = process_and_predict(df_temporal)
            logging.info(f"Happiness score predict: {prediccion}")

            df1['happiness_score_prediccion'] = prediccion
            df1.to_sql('predicciones', engine, if_exists='append', index=False)
            logging.info("Datos guardados en la base de datos")
        except KeyError as e:
            logging.error(f"Missing columns in the data: {e}")


if __name__ == "__main__":
    kafka_producer()
    kafka_consumer()