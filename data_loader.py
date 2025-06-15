import pandas as pd

file_path = "data/pacific_island_countries_data.csv"
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Filter kolom relevan
    cols_to_keep = [
        'INDICATOR', 'Indicator', 'GEO_PICT', 'Pacific Island Countries and territories',
        'SEX', 'Sex', 'AGE', 'Age', 'URBANIZATION', 'Urbanization',
        'TIME_PERIOD', 'Time', 'OBS_VALUE', 'Observation value',
        'UNIT_MEASURE', 'Unit of measure', 'DATA_SOURCE', 'Data source'
    ]
    df = df[cols_to_keep]

    # Clean data
    df = df.rename(columns={
        'GEO_PICT': 'Country_Code',
        'Pacific Island Countries and territories': 'Country',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Value'
    })

    # Konversi tipe data
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Filter tahun valid
    df = df[df['Year'] >= 2000]

    # Handle missing values
    df['Sex'] = df['Sex'].fillna('Total')
    df['Age'] = df['Age'].fillna('All ages')
    df['Urbanization'] = df['Urbanization'].fillna('National')

    return df