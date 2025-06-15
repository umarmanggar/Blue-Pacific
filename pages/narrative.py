from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np # Kita butuh numpy untuk logaritma
from data_loader import load_data

# Muat data sekali saja
df, geojson_data = load_data()

# --- PERSIAPAN DATA UNTUK SETIAP "BAB" CERITA ---
indikator_bab_1 = "IT_NET_BBND"
indikator_bab_2 = "IT_MOB_4GNTWK"
indikator_bab_3 = "BPI_PRU"

df_map = df[df['Indicator'] == indikator_bab_1]
df_map_latest = df_map.loc[df_map.groupby('Country')['Year'].idxmax()] if not df_map.empty else pd.DataFrame()

# =====================================================================
# === PERUBAHAN UTAMA UNTUK SKALA LOGARITMIK ===
if not df_map_latest.empty:
    # Buat kolom baru berisi logaritma dari 'Value'
    # Kita tambahkan 1 agar nilai 0 tidak error saat di-log
    df_map_latest['LogValue'] = np.log10(df_map_latest['Value'] + 1)
# =====================================================================

df_coverage = df[df['Indicator'] == indikator_bab_2]
df_coverage_latest = df_coverage.loc[df_coverage.groupby('Country')['Year'].idxmax()] if not df_coverage.empty else pd.DataFrame()

df_price = df[df['Indicator'] == indikator_bab_3]
df_price_latest = df_price.loc[df_price.groupby('Country')['Year'].idxmax()] if not df_price.empty else pd.DataFrame()


# --- MEMBUAT FIGUR ---
if not df_map_latest.empty:
    # Gunakan 'LogValue' untuk pewarnaan, tapi tampilkan 'Value' asli di hover
    fig_map = px.choropleth(df_map_latest, geojson=geojson_data, locations='iso_alpha',
                           featureidkey="properties.ISO_A3",
                           color='LogValue', # <-- Gunakan kolom LogValue untuk warna
                           color_continuous_scale="Blues",
                           hover_name='Country',
                           # Tampilkan Value asli, bukan LogValue
                           hover_data={'Value': ':.2f', 'Year': True, 'LogValue': False},
                           labels={'LogValue': 'Value (Log Scale)'}) # Label untuk legenda

    fig_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
else:
    fig_map = go.Figure().add_annotation(text="Data tidak tersedia untuk indikator ini", show_arrow=False)

# ... (sisa kode untuk fig_coverage dan fig_price tetap sama) ...
if not df_coverage_latest.empty:
    fig_coverage = px.bar(df_coverage_latest.sort_values('Value', ascending=True), x='Value', y='Country', orientation='h', labels={'Value': '% Populasi Terjangkau Sinyal', 'Country': ''}, text='Value')
    fig_coverage.update_traces(texttemplate='%{text:.2s}%', textposition='inside', marker_color='#0066cc')
else:
    fig_coverage = go.Figure().add_annotation(text="Data tidak tersedia", show_arrow=False)

if not df_price_latest.empty:
    fig_price = px.bar(df_price_latest.sort_values('Value', ascending=False), x='Value', y='Country', orientation='h', labels={'Value': 'Harga Layanan (% GNI)', 'Country': ''}, text='Value')
    fig_price.update_traces(texttemplate='%{text:.2f}%', textposition='auto', marker_color='#cc6600')
else:
    fig_price = go.Figure().add_annotation(text="Data tidak tersedia", show_arrow=False)


# --- LAYOUT HALAMAN NARATIF ---
layout = dbc.Container([
    dbc.Row(dbc.Col(html.Div([html.H1("Menavigasi Konektivitas Digital di Blue Pacific", className="display-4"), html.P("Sebuah Tinjauan Visual Mengenai Perkembangan Teknologi dan Konektivitas di Negara-Negara Kepulauan Pasifik.", className="lead text-muted"), html.Hr(className="my-4")]), width=12, className="text-center my-5")),
    dbc.Row([dbc.Col([html.H3("Peta Sebaran Indikator"), dcc.Markdown("Peta di bawah ini menunjukkan sebaran **indikator terpilih** pada tahun data terakhir yang tersedia. Warna yang lebih gelap menandakan nilai yang lebih tinggi.")], md=4), dbc.Col(dcc.Graph(figure=fig_map, config={'displayModeBar': False}), md=8)], className="align-items-center mb-5"),
    dbc.Row([dbc.Col(dcc.Graph(figure=fig_coverage, config={'displayModeBar': False}), md=8), dbc.Col([html.H3("Jangkauan Jaringan"), dcc.Markdown("Grafik ini menampilkan **persentase populasi yang dijangkau oleh jaringan seluler**. Jangkauan yang luas adalah fondasi untuk ekonomi digital.")], md=4)], className="align-items-center mb-5"),
    dbc.Row([dbc.Col([html.H3("Keterjangkauan Biaya"), dcc.Markdown("Grafik di bawah mengilustrasikan **biaya paket layanan seluler**. Angka yang lebih **rendah** berarti layanan lebih terjangkau.")], md=4), dbc.Col(dcc.Graph(figure=fig_price, config={'displayModeBar': False}), md=8)], className="align-items-center mb-5"),
], fluid=False, style={'maxWidth': '1000px'})