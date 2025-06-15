import pandas as pd

def load_and_preprocess_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return pd.DataFrame()

    # Pastikan kolom yang diperlukan ada
    required_columns = [
        'INDICATOR', 'Indicator', 'GEO_PICT', 'Pacific Island Countries and territories',
        'SEX', 'Sex', 'AGE', 'Age', 'URBANIZATION', 'Urbanization',
        'TIME_PERIOD', 'Time', 'OBS_VALUE', 'Observation value'
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns - {', '.join(missing_cols)}")
        return pd.DataFrame()

    # Filter kolom relevan
    df = df[required_columns]

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