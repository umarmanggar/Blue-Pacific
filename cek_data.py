# cek_data.py

import pandas as pd

# Salin fungsi preprocess_data persis seperti yang ada di app_narrative.py
def preprocess_data(df):
    if df.empty:
        return df
    rename_map = {
        'INDICATOR': 'Indicator', 'GEO_PICT': 'Country', 'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Value', 'SEX': 'Sex', 'AGE': 'Age', 'URBANIZATION': 'Urbanization'
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Year', 'Value'], inplace=True)
    df['Year'] = df['Year'].astype(int)
    country_mapping = {
        "Cook Islands": "COK", "Fiji": "FJI", "Kiribati": "KIR", "Marshall Islands": "MHL",
        "Micronesia (Federated States of)": "FSM", "Nauru": "NRU", "Niue": "NIU", "Palau": "PLW",
        "Samoa": "WSM", "Tonga": "TON", "Tuvalu": "TUV", "Vanuatu": "VUT"
    }
    df['iso_alpha'] = df['Country'].map(country_mapping)
    return df

print("="*50)
print("MEMULAI SKRIP DIAGNOSIS: cek_data.py")
print("="*50)

try:
    # --- LANGKAH A: Muat Data ---
    print("1. Mencoba memuat file CSV...")
    df = pd.read_csv("Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv")
    print("   -> OK: File CSV berhasil dimuat.")

    # --- LANGKAH B: Proses Data ---
    print("2. Memproses data dengan fungsi preprocess_data...")
    df = preprocess_data(df)
    print("   -> OK: Data berhasil diproses.")

    # --- LANGKAH C: Reset Indeks (Langkah Kunci) ---
    print("3. Mengecek kondisi indeks SEBELUM reset...")
    print(f"   -> Apakah indeks unik? {df.index.is_unique}")

    print("4. Mereset indeks...")
    df.reset_index(drop=True, inplace=True)

    print("5. Mengecek kondisi indeks SETELAH reset...")
    print(f"   -> Apakah indeks unik? {df.index.is_unique}")

    # --- LANGKAH D: Coba Filter (Baris yang sering menyebabkan error) ---
    print("6. Mencoba melakukan filter pada indikator...")
    nama_indikator = "Mobile cellular subscriptions (per 100 people)"

    # Cek apakah kolom 'Indicator' ada
    if 'Indicator' not in df.columns:
        raise KeyError("Kolom 'Indicator' tidak ditemukan di DataFrame. Cek nama kolom di file CSV.")

    df_map = df[df['Indicator'] == nama_indikator]
    print("   -> OK: Filter BERHASIL.")
    print(f"   -> Ditemukan {len(df_map)} baris untuk indikator tersebut.")

    print("\n" + "="*50)
    print("SKRIP SELESAI TANPA ERROR. Pemrosesan data Anda AMAN.")
    print("="*50)

except Exception as e:
    print("\n" + "!"*50)
    print("!!! TERJADI ERROR SELAMA DIAGNOSIS !!!")
    print("!"*50)
    print(f"Jenis Error: {type(e).__name__}")
    print(f"Pesan Error: {e}")
    import traceback
    traceback.print_exc()