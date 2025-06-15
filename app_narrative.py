# app_narrative.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd
import json

# --- 1. INISIALISASI DAN MEMUAT DATA ---

# Gunakan tema yang bersih dan modern
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "The State of Connectivity in the Blue Pacific"
server = app.server

# Muat data CSV dan GeoJSON
try:
    df = pd.read_csv("Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv")
    with open("data/countries.geojson", 'r') as f:
        geojson_data = json.load(f)
except Exception as e:
    print(f"Error loading data: {e}")
    # Jika data gagal dimuat, tampilkan pesan error
    app.layout = dbc.Alert("Error loading data files. Please check file paths and content.", color="danger")
    # Hentikan eksekusi lebih lanjut jika data tidak ada
    # Anda bisa juga menjalankan `if __name__ == '__main__':` di bawah `else`
    # tapi ini lebih eksplisit.
    # Untuk menjalankan, Anda harus pastikan data ada.

# Panggil fungsi untuk membersihkan data
def preprocess_data(df):
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

df = preprocess_data(df)


# --- 2. PERSIAPAN DATA UNTUK SETIAP "BAB" CERITA ---

# Bab 1: Data untuk Peta Langganan Seluler
df_map = df[df['Indicator'] == "Mobile cellular subscriptions (per 100 people)"]
df_map_latest = df_map.loc[df_map.groupby('Country')['Year'].idxmax()]
df.reset_index(drop=True, inplace=True)

# Bab 2: Data untuk Jangkauan Sinyal
df_coverage = df[df['Indicator'] == "% of population covered by at least a 3G mobile network"]
df_coverage_latest = df_coverage.loc[df_coverage.groupby('Country')['Year'].idxmax()]

# Bab 3: Data untuk Harga Layanan
df_price = df[df['Indicator'] == "Mobile-cellular services price basket (% of GNI per capita)"]
df_price_latest = df_price.loc[df_price.groupby('Country')['Year'].idxmax()]


# --- 3. MEMBUAT FIGUR PLOTLY UNTUK SETIAP GRAFIK ---

# Grafik Peta untuk Bab 1
fig_map = px.choropleth(
    df_map_latest,
    geojson=geojson_data,
    locations='iso_alpha',
    featureidkey="properties.ISO_A3",
    color='Value',
    color_continuous_scale="Blues",
    hover_name='Country',
    hover_data={'Value': ':.2f', 'Year': True},
    labels={'Value': 'Langganan per 100 orang'}
)
fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    coloraxis_colorbar_title_text=''
)

# Grafik Batang untuk Bab 2 (Jangkauan)
fig_coverage = px.bar(
    df_coverage_latest.sort_values('Value', ascending=True),
    x='Value',
    y='Country',
    orientation='h',
    labels={'Value': '% Populasi Terjangkau Sinyal 3G', 'Country': ''},
    text='Value' # Menampilkan nilai di dalam bar
)
fig_coverage.update_traces(texttemplate='%{text:.2s}%', textposition='inside', marker_color='#0066cc')
fig_coverage.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# Grafik Batang untuk Bab 3 (Harga)
fig_price = px.bar(
    df_price_latest.sort_values('Value', ascending=False),
    x='Value',
    y='Country',
    orientation='h',
    labels={'Value': 'Harga Layanan (% dari GNI per kapita)', 'Country': ''},
    text='Value'
)
fig_price.update_traces(texttemplate='%{text:.2f}%', textposition='auto', marker_color='#cc6600')


# --- 4. MENYUSUN LAYOUT NARATIF ---

app.layout = dbc.Container([
    # PROLOG
    dbc.Row(
        dbc.Col(
            html.Div([
                html.H1("Menavigasi Konektivitas Digital di Blue Pacific", className="display-4"),
                html.P(
                    "Sebuah Tinjauan Visual Mengenai Perkembangan Teknologi dan Konektivitas di Negara-Negara Kepulauan Pasifik.",
                    className="lead text-muted"
                ),
                html.Hr(className="my-4")
            ]),
            width=12,
            className="text-center my-5"
        )
    ),

    # BAB 1: PETA
    dbc.Row([
        dbc.Col([
            html.H3("Peta Langganan Seluler: Gambaran Umum"),
            dcc.Markdown("""
                Langkah pertama dalam memahami lanskap digital adalah melihat seberapa banyak orang yang sudah terhubung.
                Peta di bawah ini menunjukkan jumlah **langganan seluler per 100 penduduk** pada tahun data terakhir yang tersedia.
                Warna yang lebih gelap menandakan tingkat penetrasi yang lebih tinggi. Arahkan kursor ke sebuah negara untuk melihat detailnya.
            """),
        ], md=4),
        dbc.Col(dcc.Graph(figure=fig_map, config={'displayModeBar': False}), md=8),
    ], className="align-items-center mb-5"),

    # BAB 2: JANGKAUAN
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_coverage, config={'displayModeBar': False}), md=8),
        dbc.Col([
            html.H3("Jangkauan Jaringan: Siapa yang Terhubung?"),
            dcc.Markdown("""
                Memiliki telepon tidak cukup jika tidak ada sinyal. Grafik ini menampilkan **persentase populasi yang dijangkau
                oleh setidaknya jaringan seluler 3G**. Jangkauan yang luas adalah fondasi untuk ekonomi digital.
                Negara dengan bar yang lebih panjang memiliki infrastruktur yang lebih merata.
            """),
        ], md=4),
    ], className="align-items-center mb-5"),

    # BAB 3: HARGA
    dbc.Row([
        dbc.Col([
            html.H3("Keterjangkauan: Biaya untuk Tetap Terhubung"),
            dcc.Markdown("""
                Setelah infrastruktur ada, pertanyaan berikutnya adalah: *apakah masyarakat mampu membayarnya?*
                Grafik di bawah mengilustrasikan **biaya paket layanan seluler sebagai persentase dari Pendapatan Nasional Bruto (GNI)
                per kapita**. Angka yang lebih **rendah** berarti layanan lebih terjangkau bagi rata-rata penduduk.
            """),
        ], md=4),
        dbc.Col(dcc.Graph(figure=fig_price, config={'displayModeBar': False}), md=8),
    ], className="align-items-center mb-5"),

    # EPILOG
    dbc.Row(
        dbc.Col([
            html.Hr(),
            html.P("Dasbor ini menunjukkan bahwa perjalanan digital di Pasifik memiliki banyak sisi. Meskipun beberapa negara unggul dalam penetrasi, tantangan tetap ada dalam hal jangkauan infrastruktur dan keterjangkauan biaya. Strategi Blue Pacific 2050 bertujuan untuk mengatasi tantangan ini secara kolaboratif.",
                   className="text-center text-muted mt-3"),
            html.P([
                "Dibuat untuk Pacific Data Viz Challenge | Data: ",
                html.A("Pacific Data Hub", href="https://stats.pacificdata.org/", target="_blank"),
            ], className="text-center small")
        ], width=12)
    )

], fluid=False, style={'maxWidth': '1000px'}) # Mengatur lebar maksimal untuk tampilan seperti artikel


# --- 5. MENJALANKAN APLIKASI ---
if __name__ == '__main__':
    # Pastikan data berhasil dimuat sebelum menjalankan server
    if 'df' in locals():
        app.run_server(debug=True)