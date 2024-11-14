# Workshop #3: Machine Learning and Data Streaming <img src="https://github.com/user-attachments/assets/e50b269a-fd97-4ec3-a1e9-e9629cef94ae" alt="Data Icon" width="30px"/>

Realized by **Juan Andrés Ruiz Muñoz** ([@JuanRuizIng](https://github.com/JuanRuizIng)).

## Overview ✨

In this workshop, we use data about happiness scores from various countries to train a machine learning regression model. With this model, we aim to predict the happiness score. The workshop involves executing a complete EDA/ETL pipeline to extract features from the data, training the model with a 70-30 data split (70% for training and 30% for testing), streaming the transformed data, and using a consumer to retrieve the data and employ the trained model for prediction. Predictions, along with respective input features, are stored in a database. Finally, a performance metric is extracted to evaluate the model, as shown in the following figure:

![image](https://github.com/user-attachments/assets/071f476d-c208-46ac-a0d2-59610705a121)


## Expectations

The goal is to train a regression model with all EDA and feature selection steps, stream the data using Kafka, use the trained model to predict values in the testing dataset, and extract a performance metric for model evaluation.

## Data <img src="https://github.com/user-attachments/assets/5fa5298c-e359-4ef1-976d-b6132e8bda9a" alt="Dataset" width="30px"/>

The data consists of five CSV files with happiness information from various countries across different years. Due to structural differences between datasets, each year's data was cleaned, standardized, and concatenated into a unified DataFrame. The following columns were retained and renamed for consistency:

- **happiness_rank**: The overall rank of happiness for each country.
- **country**: Name of the country or region.
- **happiness_score**: The happiness score, based on various socioeconomic indicators.
- **gdp_per_capita**: GDP per capita, reflecting the country's economic output per person.
- **family**: Social support or family index, indicating the level of social connections.
- **health**: Life expectancy or healthy life index, showing the average expected lifespan.
- **freedom**: Freedom to make life choices, measuring personal freedom.
- **generosity**: The generosity score, which reflects the population's willingness to give.
- **trust_government_corruption**: Perception of corruption, representing the level of public trust in the government.

Each data file was cleaned as follows:

1. **2015**: Dropped unnecessary columns such as `Standard Error`, `Dystopia Residual`, and `Region`, and renamed columns for consistency.
2. **2016**: Removed `Lower Confidence Interval`, `Upper Confidence Interval`, `Dystopia Residual`, and `Region`, and applied consistent column naming.
3. **2017**: Dropped `Whisker.high`, `Whisker.low`, and `Dystopia.Residual`, and renamed columns.
4. **2018-2019**: Unified column names such as `Country or region` to `country` and `Score` to `happiness_score`.

## Technologies ✨

The following tools and technologies are expected to be used for this workshop:

- Python ➜ [Download site](https://www.python.org/downloads/)
- Jupyter Notebook ➜ [VS Code tool for using notebooks](https://youtu.be/ZYat1is07VI?si=BMHUgk7XrJQksTkt)
- Database (any of your choice)
- Kafka ➜ [Download and setup](https://kafka.apache.org/downloads)
- Scikit-learn [Documentation](https://scikit-learn.org/stable/index.html)
- Docker [Documentation](https://docs.docker.com/)

## Running the code ⏯️

### Clone the repository

Execute the following command to clone the repository:

```bash
https://github.com/JuanRuizIng/Workshop003_Data_and_AI_Engineering.git
```

### Enviromental variables

To establish the connection to the database, we use a module called *db_operations.py*. In this Python script we call a file where our environment variables are stored, this is how we will create this file:

1. We create a directory named ***env*** inside the workspace.

2. There we create a file called ***.env***.

3. In that file we declare 6 enviromental variables. Remember that the variables in this case go without double quotes, i.e. the string notation (`"`):
   ```python
    PG_HOST = # host address, e.g. localhost or 127.0.0.1
    PG_PORT = # PostgreSQL port, e.g. 5432

    PG_USER = # your PostgreSQL user
    PG_PASSWORD = # your user password
    
    PG_DATABASE = # your database name, e.g. postgres
   ```

### Data input

For data streaming to take place, the 5 files must be placed in a folder.

1. We create a directory named *data* inside the workspace.

2. There you put the csv files.

### Running the code

> [!NOTE]
> Notebooks are omitted, because the model is already in the artifacts. If you need to see the model detail and the EDA the notebooks will be organized in an orderly fashion in the *notebooks* folder.

#### To start the kafka consumer

1. Start the containers
```bash
docker compose up -d
```

2. Access to the container
```bash
docker exec -it workshop003_kafka bash
```

3. Create a new topic
```bash
kafka-topics --bootstrap-server workshop003_kafka:9092 --create --topic workshop003_streaming_topic
```

4. Listener the messages
```bash
kafka-console-consumer --bootstrap-server workshop003_kafka:9092 --topic workshop003_streaming_topic --from-beginning
```

#### To start the kafka producer

1. Configure poetry and libraries install
```bash
poetry shell
poetry install
```

2. Run main.py
```bash
python main.py
```

### Results

* In the kafka consumer:

![image](https://github.com/user-attachments/assets/af633254-53bf-44c5-ba1b-18024e918169)

* In the kafka producer:

![image](https://github.com/user-attachments/assets/5fa531e6-85b5-4518-a226-89cbf66a4c22)

* In the database:

![image](https://github.com/user-attachments/assets/c58d4d71-9f8e-4d03-b24c-f5bf7f52a83d)


## Thank you! 💻
