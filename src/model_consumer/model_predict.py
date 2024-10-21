from kafka import KafkaConsumer
import json
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


with open('modelo_entrenado.pkl', 'rb') as f:
    model = pickle.load(f)


def process_and_predict(data):
    """
    Procesa los datos consumidos y realiza la predicción usando el modelo.
    """
    # Convertir el mensaje consumido a un DataFrame o el formato adecuado según el modelo
    df = pd.DataFrame([data])
    
    # Asegurarse de que las columnas coinciden con las características usadas para entrenar el modelo
    # Aquí puedes hacer cualquier preprocesamiento que sea necesario, por ejemplo, eliminar columnas
    # o ajustar los tipos de datos.
    X = df.drop(['happiness_score', 'country'], axis=1)
    
    # Realizar la predicción
    prediccion = model.predict(X)
    
    # Retornar la predicción junto con los datos originales (si es necesario para guardarlos)
    return prediccion[0], df
