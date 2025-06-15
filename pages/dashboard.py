from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data

# Muat data sekali
df, _ = load_data()

# Ambil daftar unik untuk filter dari data yang bersih
# Kita menggunakan kode indikator, bukan nama panjang
indicators = sorted(df['Indicator'].unique())
# Kita menggunakan kode negara 2 huruf
countries = sorted(df['Country'].unique())

layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Dasbor Eksplorasi Data", className="text-center my-4"))),

    # Filter
    dbc.Row(dbc.Col(dbc.Card([dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label("Pilih Indikator:", className="fw-bold"),
                dcc.Dropdown(id='indicator-dropdown', options=indicators, value=indicators[0])
            ], md=6),
            dbc.Col([
                html.Label("Pilih Negara:", className="fw-bold"),
                dcc.Dropdown(id='country-dropdown', options=countries, value=countries[:5], multi=True)
            ], md=6)
        ]),
        dbc.Row(dbc.Col([
            html.Label("Pilih Rentang Tahun:", className="fw-bold mt-3"),
            dcc.RangeSlider(id='year-range-slider', min=df['Year'].min(), max=df['Year'].max(), step=1,
                            marks={year: str(year) for year in range(df['Year'].min(), df['Year'].max() + 1, 2)},
                            value=[df['Year'].min() + 5, df['Year'].max()])
        ]), className="mt-3")
    ])]), className="mb-4")),

    # Grafik
    dbc.Row([
        dbc.Col(dcc.Graph(id='dashboard-line-chart'), md=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='dashboard-bar-chart'), md=12)
    ])
], fluid=True)

@callback(
    Output('dashboard-line-chart', 'figure'),
    Output('dashboard-bar-chart', 'figure'),
    Input('indicator-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('year-range-slider', 'value')
)
def update_dashboard_charts(indicator, countries, year_range):
    if not indicator or not countries or not year_range:
        no_data_fig = go.Figure().add_annotation(text="Please select all filters", showarrow=False)
        return no_data_fig, no_data_fig

    filtered_df = df[
        (df['Indicator'] == indicator) &
        (df['Country'].isin(countries)) &
        (df['Year'].between(year_range[0], year_range[1]))
    ]

    if filtered_df.empty:
        no_data_fig = go.Figure().add_annotation(text="No data available for this selection", showarrow=False)
        return no_data_fig, no_data_fig

    # Line Chart
    line_fig = px.line(filtered_df, x='Year', y='Value', color='Country', markers=True,
                       title=f"Tren Tahunan: {indicator}")

    # Bar Chart (Perbandingan di tahun terakhir yang tersedia)
    latest_df = filtered_df.loc[filtered_df.groupby('Country')['Year'].idxmax()]
    bar_fig = px.bar(latest_df, x='Country', y='Value', color='Country',
                     title=f"Perbandingan di Tahun Terakhir ({latest_df['Year'].max()}): {indicator}")

    return line_fig, bar_fig