# callbacks.py

from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# Tandatangan fungsi diubah untuk menerima geojson_data
def register_callbacks(app, data, geojson_data):
    @callback(
        Output('time-series-plot', 'figure'),
        Output('comparison-plot', 'figure'),
        Output('map-plot', 'figure'),
        Output('metrics-display', 'children'),
        Input('indicator-selector', 'value'),
        Input('country-selector', 'value'),
        Input('year-slider', 'value')
    )
    def update_visuals(selected_indicator, selected_countries, year_range):
        from dash import html

        no_data_fig = go.Figure()
        no_data_fig.update_layout(
            xaxis={'visible': False}, yaxis={'visible': False},
            annotations=[{'text': 'No data for selection', 'xref': 'paper', 'yref': 'paper', 'showarrow': False, 'font': {'size': 16}}]
        )

        if not selected_countries:
            no_data_fig.update_layout(annotations=[{'text': 'Please select a country'}])
            return no_data_fig, no_data_fig, no_data_fig, []

        filtered_df = data[
            (data['Indicator'] == selected_indicator) &
            (data['Country'].isin(selected_countries)) &
            (data['Year'].between(year_range[0], year_range[1]))
        ].copy()

        if filtered_df.empty:
            return no_data_fig, no_data_fig, no_data_fig, []

        # --- Grafik Tren dan Perbandingan (Tetap Sama) ---
        fig_time = px.line(
            filtered_df.sort_values('Year'), x='Year', y='Value', color='Country', markers=True,
            title=f'<b>Trend: {selected_indicator}</b>'
        )
        fig_time.update_layout(transition_duration=500, legend_title_text='Country', margin=dict(t=50))

        latest_year_df = filtered_df.loc[filtered_df.groupby('Country')['Year'].idxmax()]
        fig_bar = px.bar(
            latest_year_df.sort_values('Value', ascending=True), y='Country', x='Value', color='Country',
            title=f'<b>Comparison in Latest Year ({latest_year_df["Year"].max()})</b>', orientation='h'
        )
        fig_bar.update_layout(transition_duration=500, showlegend=False, margin=dict(t=50))
        fig_bar.update_yaxes(title_text="")

        # --- PEMBARUAN PENTING PADA PETA GEOGRAFIS ---
        fig_map = px.choropleth(
            latest_year_df,
            geojson=geojson_data,                       # 1. Gunakan file GeoJSON Anda
            locations='iso_alpha',                      # 2. Kolom di dataframe Anda untuk dicocokkan
            featureidkey="properties.ISO_A3",           # 3. Path ke ID unik di file GeoJSON (biasanya kode ISO 3 huruf)
            color='Value',
            color_continuous_scale="Viridis",
            hover_name='Country',
            hover_data={'Value': ':.2f', 'Year': True}
        )
        # 4. Sesuaikan tampilan peta agar fokus ke lokasi yang relevan
        fig_map.update_geos(fitbounds="locations", visible=False)
        fig_map.update_layout(
            title_text='<b>Geographical Distribution</b>',
            margin={"r":0, "t":50, "l":0, "b":0},
            transition_duration=500,
            coloraxis_colorbar_title_text='Value'
        )

        # --- Kartu Metrik (Tetap Sama) ---
        avg_value = filtered_df['Value'].mean()
        max_row = filtered_df.loc[filtered_df['Value'].idxmax()]
        metrics = [
            dbc.Card(dbc.CardBody([html.H4("Average Value", className="card-title"), html.P(f"{avg_value:,.2f}", className="card-text fs-3")]), className="mb-3", color="light"),
            dbc.Card(dbc.CardBody([html.H4("Highest Value", className="card-title"), html.P(f"{max_row['Value']:,.2f}", className="card-text fs-3"), html.Small(f"{max_row['Country']} ({max_row['Year']})", className="text-muted")]), className="mb-3", color="light"),
        ]

        return fig_time, fig_bar, fig_map, metrics