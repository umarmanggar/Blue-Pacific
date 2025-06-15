import pandas as pd
import json

def load_and_preprocess_data(file_path):
    """
    Memuat dan membersihkan data dari file CSV. (Fungsi ini tetap sama)
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    except Exception as e:
        print(f"Error memuat data: {e}")
        return pd.DataFrame()

    rename_map = {
        'INDICATOR': 'Indicator',
        'GEO_PICT': 'Country',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Value',
        'SEX': 'Sex',
        'AGE': 'Age',
        'URBANIZATION': 'Urbanization'
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Year', 'Value'], inplace=True)
    df['Year'] = df['Year'].astype(int)

    for col in ['Sex', 'Age', 'Urbanization']:
        if col in df.columns:
            df[col] = df[col].fillna('Not Specified')

    # Kolom 'iso_alpha' ini menjadi SANGAT PENTING untuk menghubungkan data Anda dengan GeoJSON
    country_mapping = {
        "Cook Islands": "COK", "Fiji": "FJI", "Kiribati": "KIR",
        "Marshall Islands": "MHL", "Micronesia (Federated States of)": "FSM",
        "Nauru": "NRU", "Niue": "NIU", "Palau": "PLW", "Samoa": "WSM",
        "Tonga": "TON", "Tuvalu": "TUV", "Vanuatu": "VUT"
    }
    if 'Country' in df.columns:
        df['iso_alpha'] = df['Country'].map(country_mapping)

    return df

# --- FUNGSI BARU DITAMBAHKAN ---
def load_geojson(file_path):
    """
    Memuat data GeoJSON dari file.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error memuat file GeoJSON: {e}")
        return None