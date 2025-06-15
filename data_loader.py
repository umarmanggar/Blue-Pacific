import pandas as pd
import os
import json

def load_and_preprocess_data(file_path):
    try:
        # Coba beberapa encoding
        for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Successfully loaded with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("Failed to determine file encoding")
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

    # Kolom yang akan dipertahankan
    cols_to_keep = [
        'INDICATOR', 'Indicator', 'GEO_PICT', 'Pacific Island Countries and territories',
        'SEX', 'Sex', 'AGE', 'Age', 'URBANIZATION', 'Urbanization',
        'TIME_PERIOD', 'Time', 'OBS_VALUE', 'Observation value'
    ]

    # Filter kolom yang ada
    available_cols = [col for col in cols_to_keep if col in df.columns]
    df = df[available_cols]

    # Rename kolom
    rename_map = {
        'GEO_PICT': 'Country_Code',
        'Pacific Island Countries and territories': 'Country',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Value'
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Konversi tipe data
    if 'Year' in df.columns:
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    if 'Value' in df.columns:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # Handle missing values
    if 'Sex' in df.columns:
        df['Sex'] = df['Sex'].fillna('Total')
    if 'Age' in df.columns:
        df['Age'] = df['Age'].fillna('All ages')
    if 'Urbanization' in df.columns:
        df['Urbanization'] = df['Urbanization'].fillna('National')

    # Filter tahun
    if 'Year' in df.columns:
        df = df[(df['Year'] >= 2000) & (df['Year'] <= 2024)]

    # Tambahkan kode negara ISO
    country_mapping = {
        "Cook Islands": "COK",
        "Samoa": "WSM",
        "Fiji": "FJI",
        "Micronesia (Federated States of)": "FSM",
        "Tuvalu": "TUV",
        "Vanuatu": "VUT",
        "Nauru": "NRU",
        "Kiribati": "KIR",
        "Tonga": "TON",
        "Marshall Islands": "MHL",
        "Palau": "PLW",
        "Niue": "NIU",
        "Solomon Islands": "SLB",
        "French Polynesia": "PYF"
    }

    df['ISO'] = df['Country'].map(country_mapping)

    return df

def load_geojson():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        geojson_path = os.path.join(base_dir, 'data', 'countries.geojson')

        with open(geojson_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return None