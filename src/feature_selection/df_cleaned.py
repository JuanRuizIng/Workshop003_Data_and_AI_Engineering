import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_and_concat_csv_data():
    """ Data cleaning and concat of CSV files 
    Parameters:
    None
    
    Returns:
    df (pandas.DataFrame): DataFrame with the cleaned data.
    """

    
    df_2015 = pd.read_csv('data/2015.csv')
    df_2016 = pd.read_csv('data/2016.csv')
    df_2017 = pd.read_csv('data/2017.csv')
    df_2018 = pd.read_csv('data/2018.csv')
    df_2019 = pd.read_csv('data/2019.csv')
    df_2015 = df_2015.drop(['Standard Error', 'Dystopia Residual', 'Region'], axis=1)
    columns_rename = {
        'Economy (GDP per Capita)': 'gdp_per_capita',
        'Health (Life Expectancy)': 'health',
        'Trust (Government Corruption)': 'trust_government_corruption',
        'Family': 'family',
        'Freedom': 'freedom',
        'Generosity': 'generosity',
        'Happiness Rank': 'happiness_rank',
        'Happiness Score': 'happiness_score',
        'Country': 'country'
    }
    df_2015 = df_2015.rename(columns=columns_rename)
    df_2015['year'] = 2015

    df_2016 = df_2016.drop(['Lower Confidence Interval', 'Upper Confidence Interval', 'Dystopia Residual', 'Region'], axis=1)
    df_2016 = df_2016.rename(columns=columns_rename)
    df_2016['year'] = 2016

    df_2017 = df_2017.drop(['Whisker.high', 'Whisker.low', 'Dystopia.Residual'], axis=1)
    columns_rename_2017 = {
        'Economy..GDP.per.Capita.': 'gdp_per_capita',
        'Health..Life.Expectancy.': 'health',
        'Trust..Government.Corruption.': 'trust_government_corruption',
        'Family': 'family',
        'Freedom': 'freedom',
        'Generosity': 'generosity',
        'Happiness.Rank': 'happiness_rank',
        'Happiness.Score': 'happiness_score',
        'Country': 'country'
    }
    df_2017 = df_2017.rename(columns=columns_rename_2017)
    df_2017['year'] = 2017

    columns_rename_2018_2019 = {
        'Country or region': 'country',
        'GDP per capita': 'gdp_per_capita',
        'Healthy life expectancy': 'health',
        'Freedom to make life choices': 'freedom',
        'Generosity': 'generosity',
        'Perceptions of corruption': 'trust_government_corruption',
        'Social support': 'family',
        'Overall rank': 'happiness_rank',
        'Score': 'happiness_score'
    }
    df_2018 = df_2018.rename(columns=columns_rename_2018_2019)
    df_2018['year'] = 2018

    df_2019 = df_2019.rename(columns=columns_rename_2018_2019)
    df_2019['year'] = 2019

    df = pd.concat([df_2015, df_2016, df_2017, df_2018, df_2019], axis=0)
    df['trust_government_corruption'] = df['trust_government_corruption'].fillna(df['trust_government_corruption'].median())

    return df