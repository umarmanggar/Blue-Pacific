import pandas as pd

def load_and_preprocess_data(file_path):
    try:
        # Coba beberapa encoding yang umum
        for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Berhasil memuat file dengan encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            # Jika semua encoding gagal
            raise ValueError("Gagal menentukan encoding file")
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

    # Pilih kolom yang relevan
    cols_to_keep = [
        'INDICATOR', 'Indicator', 'GEO_PICT', 'Pacific Island Countries and territories',
        'SEX', 'Sex', 'AGE', 'Age', 'URBANIZATION', 'Urbanization',
        'TIME_PERIOD', 'Time', 'OBS_VALUE', 'Observation value'
    ]

    # Filter kolom yang ada di dataset
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

    # Filter tahun valid
    if 'Year' in df.columns:
        df = df[(df['Year'] >= 2000) & (df['Year'] <= 2024)]

    return df