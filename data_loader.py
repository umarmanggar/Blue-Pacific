import pandas as pd
import json

def load_data():
    """Memuat dan memproses semua data yang dibutuhkan."""
    try:
        df = pd.read_csv("Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv")
        with open("data/countries.geojson", 'r') as f:
            geojson_data = json.load(f)
    except Exception as e:
        print(f"Error loading data files: {e}")
        return pd.DataFrame(), None

    # --- Preprocessing ---
    rename_map = {
        'INDICATOR': 'Indicator', 'GEO_PICT': 'Country', 'TIME_PERIOD': 'Year', 'OBS_VALUE': 'Value'
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    # Hapus kolom duplikat jika ada
    df = df.loc[:,~df.columns.duplicated()]

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Year', 'Value'], inplace=True)
    df['Year'] = df['Year'].astype(int)

    # Pemetaan negara dari kode 2-huruf ke kode 3-huruf
    country_mapping = {
        "CK": "COK", "FJ": "FJI", "FM": "FSM", "KI": "KIR", "MH": "MHL", "NC": "NCL",
        "NR": "NRU", "NU": "NIU", "PF": "PYF", "PG": "PNG", "PW": "PLW", "SB": "SLB",
        "TO": "TON", "TV": "TUV", "VU": "VUT", "WS": "WSM"
    }
    if 'Country' in df.columns:
        df['iso_alpha'] = df['Country'].map(country_mapping)

    df.reset_index(drop=True, inplace=True)
    return df, geojson_data