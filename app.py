import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from data_loader import load_and_preprocess_data, load_geojson

# Konfigurasi halaman
st.set_page_config(
    page_title="Blue Pacific 2050 Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Muat CSS kustom
def load_css():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, 'assets', 'style.css')

        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                st.success("Custom CSS loaded successfully")
        else:
            # Gunakan CSS inline jika file tidak ditemukan
            inline_css = """
            <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f8ff;
                color: #003366;
            }
            h1 {
                color: #0066cc;
                border-bottom: 2px solid #0099cc;
                padding-bottom: 10px;
            }
            /* Tambahkan gaya lainnya sesuai kebutuhan */
            </style>
            """
            st.markdown(inline_css, unsafe_allow_html=True)
            st.warning("Using inline CSS as file not found")
    except Exception as e:
        st.warning(f"Failed to load CSS: {str(e)}")
        # Fallback ke CSS minimal
        st.markdown("""
        <style>
        body { font-family: Arial, sans-serif; }
        </style>
        """, unsafe_allow_html=True)

# UI Header
st.title("🌊 Blue Pacific 2050: Technology & Connectivity")
st.markdown("""
Visualizing progress in technology and connectivity across Pacific Islands based on the
[Blue Pacific 2050 Strategy](https://www.forumsec.org/2050strategy/)
""")

# Muat CSS kustom
load_css()

# Muat data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv')
    return load_and_preprocess_data(data_path)

# Muat GeoJSON
geojson_data = load_geojson()

df = load_data()

if df.empty:
    st.error("Failed to load data. Please check the data file and format.")
    st.stop()

# Sidebar untuk filter
with st.sidebar:
    st.header("Visualization Settings")

    # Pilih indikator
    indicators = sorted(df['Indicator'].unique())
    selected_indicator = st.selectbox(
        "Select Indicator:",
        options=indicators,
        index=0
    )

    # Pilih tahun
    if 'Year' in df.columns and not df['Year'].empty:
        years = sorted(df['Year'].unique())
        selected_year = st.selectbox(
            "Select Year:",
            options=years,
            index=len(years)-1  # Tahun terbaru
        )

    # Pilih jenis visualisasi
    viz_type = st.radio(
        "Visualization Type:",
        options=["Time Trend", "Country Comparison", "Demographic", "Geographical Map"],
        index=0
    )

# Filter data
if selected_indicator and selected_year:
    filtered_df = df[
        (df['Indicator'] == selected_indicator) &
        (df['Year'] == selected_year)
    ]
else:
    filtered_df = pd.DataFrame()

# Visualisasi berdasarkan pilihan
if viz_type == "Time Trend":
    st.subheader(f"Time Trend: {selected_indicator}")

    if filtered_df.empty:
        st.warning("No data available for selected filters")
    else:
        # Buat data untuk time trend
        time_df = df[
            (df['Indicator'] == selected_indicator) &
            (df['Year'] >= 2000)
        ]

        # Agregasi data
        trend_df = time_df.groupby(['Year', 'Country'], as_index=False)['Value'].mean()

        fig = px.line(
            trend_df,
            x='Year',
            y='Value',
            color='Country',
            markers=True,
            title=f'Time Trend of {selected_indicator}',
            labels={'Value': 'Value', 'Year': 'Year'}
        )
        st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Country Comparison":
    st.subheader(f"Country Comparison: {selected_indicator} ({selected_year})")

    if filtered_df.empty:
        st.warning("No data available for selected filters")
    else:
        # Agregasi data
        comparison_df = filtered_df.groupby('Country', as_index=False)['Value'].mean()

        fig = px.bar(
            comparison_df.sort_values('Value', ascending=True),
            x='Value',
            y='Country',
            orientation='h',
            title=f'Comparison of {selected_indicator}',
            labels={'Value': 'Value', 'Country': 'Country'},
            color='Value',
            color_continuous_scale='Teal'
        )
        st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Demographic":
    st.subheader(f"Demographic Distribution: {selected_indicator} ({selected_year})")

    if filtered_df.empty:
        st.warning("No data available for selected filters")
    elif 'Sex' not in filtered_df.columns or 'Age' not in filtered_df.columns:
        st.info("Demographic data not available for this indicator")
    else:
        # Buat pie chart untuk demografi
        fig = px.sunburst(
            filtered_df,
            path=['Sex', 'Age', 'Urbanization'],
            values='Value',
            title='Demographic Distribution',
            color='Value',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Geographical Map" and geojson_data:
    st.subheader(f"Geographical Distribution: {selected_indicator} ({selected_year})")

    if filtered_df.empty:
        st.warning("No data available for selected filters")
    else:
        # Agregasi data
        map_df = filtered_df.groupby(['ISO', 'Country'], as_index=False)['Value'].mean()

        # Buat peta koroplet
        fig = px.choropleth(
            map_df,
            geojson=geojson_data,
            locations='ISO',
            color='Value',
            hover_name='Country',
            hover_data=['Value'],
            projection='natural earth',
            title=f'Geographical Distribution of {selected_indicator}',
            color_continuous_scale='Blues'
        )

        # Sesuaikan tampilan peta
        fig.update_geos(
            visible=False,
            resolution=50,
            showcountries=True,
            countrycolor="Black",
            showcoastlines=True,
            coastlinecolor="LightBlue",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="Blue"
        )

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
elif viz_type == "Geographical Map":
    st.warning("Geojson data not available for map visualization")

# Tambahkan metrik utama
if not filtered_df.empty:
    avg_value = filtered_df['Value'].mean()
    max_value = filtered_df['Value'].max()
    min_value = filtered_df['Value'].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Value", f"{avg_value:.2f}")
    col2.metric("Highest Value", f"{max_value:.2f}")
    col3.metric("Lowest Value", f"{min_value:.2f}")

# Footer
st.markdown("---")
st.markdown("""
**Data Source:** [Pacific Data Hub](https://stats.pacificdata.org/) |
**Blue Pacific 2050 Strategy** [Learn More](https://www.forumsec.org/2050strategy/)
""")