import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from data_loader import load_and_preprocess_data

# Konfigurasi halaman
st.set_page_config(
    page_title="Blue Pacific 2050 Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Muat CSS kustom
def load_css(file_name):
    # Cari path absolut file CSS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(base_dir, file_name)

    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            st.success(f"CSS kustom berhasil dimuat dari: {css_path}")
    except FileNotFoundError:
        st.warning(f"File CSS tidak ditemukan di: {css_path}")
    except Exception as e:
        st.warning(f"Gagal memuat CSS: {str(e)}")

# Muat data
@st.cache_data
def load_data():
    # Cari path absolut file data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv')
    return load_and_preprocess_data(data_path)

# UI Header
st.title("🌊 Blue Pacific 2050: Technology & Connectivity")
st.markdown("""
Visualisasi data untuk memantau perkembangan teknologi dan konektivitas di kawasan Pasifik
sesuai dengan [Blue Pacific 2050 Strategy](https://www.forumsec.org/2050strategy/).
""")

# Muat CSS kustom - harus dipanggil sebelum konten utama
load_css('assets/style.css')

# Muat data
df = load_data()

if df.empty:
    st.error("Gagal memuat data. Mohon periksa file dan format data.")
    st.stop()

# Sidebar untuk filter
with st.sidebar:
    st.header("Pengaturan Visualisasi")

    # Pilih indikator
    indicators = sorted(df['Indicator'].unique())
    selected_indicator = st.selectbox(
        "Pilih Indikator:",
        options=indicators,
        index=0
    )

    # Pilih negara
    countries = sorted(df['Country'].unique())
    selected_countries = st.multiselect(
        "Pilih Negara:",
        options=countries,
        default=['Cook Islands', 'Samoa', 'Fiji'] if 'Cook Islands' in countries else countries[:3]
    )

    # Pilih rentang tahun
    if 'Year' in df.columns and not df['Year'].empty:
        min_year = int(df['Year'].min())
        max_year = int(df['Year'].max())
        year_range = st.slider(
            "Rentang Tahun:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    else:
        st.warning("Data tahun tidak tersedia")
        year_range = (2000, 2024)

# Filter data berdasarkan pilihan
if selected_indicator and selected_countries and year_range:
    filtered_df = df[
        (df['Indicator'] == selected_indicator) &
        (df['Country'].isin(selected_countries)) &
        (df['Year'] >= year_range[0]) &
        (df['Year'] <= year_range[1])
    ]
else:
    filtered_df = pd.DataFrame()

# Tampilan visualisasi
tab1, tab2, tab3 = st.tabs(["Tren Waktu", "Perbandingan Negara", "Distribusi Demografis"])

with tab1:
    st.subheader(f"Tren {selected_indicator}")

    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih")
    else:
        fig = px.line(
            filtered_df,
            x='Year',
            y='Value',
            color='Country',
            markers=True,
            title=f'Tren {selected_indicator}',
            labels={'Value': 'Nilai', 'Year': 'Tahun'}
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Perbandingan Antar Negara")

    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih")
    else:
        # Agregasi data untuk perbandingan
        comparison_df = filtered_df.groupby('Country', as_index=False)['Value'].mean()

        fig = px.bar(
            comparison_df.sort_values('Value', ascending=True),
            x='Value',
            y='Country',
            orientation='h',
            title='Perbandingan Rata-rata',
            labels={'Value': 'Rata-rata Nilai', 'Country': 'Negara'},
            color='Value',
            color_continuous_scale='Teal'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Distribusi Demografis")

    if filtered_df.empty:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih")
    elif 'Sex' not in filtered_df.columns or 'Age' not in filtered_df.columns:
        st.info("Data demografi tidak tersedia untuk indikator ini")
    else:
        # Buat sunburst chart
        fig = px.sunburst(
            filtered_df,
            path=['Country', 'Sex', 'Age', 'Urbanization'],
            values='Value',
            title='Distribusi Demografis',
            color='Value',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Sumber Data:** [Pacific Data Hub](https://stats.pacificdata.org/) |
**Blue Pacific 2050 Strategy** [Pelajari Lebih Lanjut](https://www.forumsec.org/2050strategy/)
""")