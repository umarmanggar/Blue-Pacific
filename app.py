# app.py

import dash
import dash_bootstrap_components as dbc
from dash import html # Import html untuk pesan error
from data_loader import load_and_preprocess_data, load_geojson
from layout import create_layout
from callbacks import register_callbacks

# --- Inisialisasi Aplikasi Dash ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Blue Pacific 2050 Dashboard"
server = app.server

# --- Memuat SEMUA Data ---
DATA_FILE = 'Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv'
GEOJSON_FILE = 'data/countries.geojson' # Path ke file GeoJSON Anda

data = load_and_preprocess_data(DATA_FILE)
geojson_data = load_geojson(GEOJSON_FILE) # Memuat GeoJSON

# --- Mengatur Layout dan Callback ---
# Cek apakah kedua data berhasil dimuat
if not data.empty and geojson_data:
    app.layout = create_layout(data)
    # Teruskan kedua data ke callbacks
    register_callbacks(app, data, geojson_data)
else:
    # Tampilkan pesan error jika salah satu data gagal dimuat
    error_message = "Gagal memuat data CSV." if data.empty else "Gagal memuat data GeoJSON."
    app.layout = html.Div([
        html.H1("Application Error"),
        html.P(f"Error: {error_message} Please check the file path and content, then restart the application.")
    ], style={'textAlign': 'center', 'padding': '50px'})

# --- Jalankan Server Aplikasi ---
if __name__ == '__main__':
    app.run_server(debug=True)