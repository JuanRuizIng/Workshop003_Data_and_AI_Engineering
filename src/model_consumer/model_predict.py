import pickle
import pandas as pd

# Cargar el modelo desde el archivo pickle
with open('artifacts/models/model.pkl', 'rb') as f:
    model = pickle.load(f)

def process_and_predict(data):
    """
    Procesa los datos consumidos y realiza la predicción usando el modelo.

    Parameters:
    data (dict): Datos consumidos desde Kafka.

    Returns:
    float: Predicción del modelo.
    """


    # Verificar si los datos ya son un DataFrame
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data)
    else:
        df = data
    
    X = df[['happiness_rank', 'gdp_per_capita', 'family', 'health', 'freedom', 'trust_government_corruption', 'generosity', 'year']]
    
    prediccion = model.predict(X)
    
    # Retornar solo la predicción
    return prediccion[0]