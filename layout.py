# layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(data):
    """
    Membuat tata letak aplikasi Dash menggunakan data yang telah diproses.
    """
    # Ambil nilai unik untuk filter dari dataframe
    unique_indicators = sorted(data['Indicator'].unique())
    unique_countries = sorted(data['Country'].unique())
    min_year, max_year = int(data['Year'].min()), int(data['Year'].max())

    # Definisikan layout dengan dbc.Container untuk tata letak yang rapi
    return dbc.Container(fluid=True, children=[
        # Baris Header
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H1("Blue Pacific 2050: Technology & Connectivity Dashboard"),
                    html.P("A Dashboard for the Pacific Data Visualization Challenge", className="text-muted")
                ]),
                width=12,
                className="text-center my-4"
            )
        ),

        # Baris Panel Kontrol (Filter)
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Indicator", className="fw-bold"),
                                dcc.Dropdown(
                                    id='indicator-selector',
                                    options=[{'label': i, 'value': i} for i in unique_indicators],
                                    value=unique_indicators[0]
                                )
                            ], md=6, className="mb-3 mb-md-0"),

                            dbc.Col([
                                html.Label("Select Countries", className="fw-bold"),
                                dcc.Dropdown(
                                    id='country-selector',
                                    options=[{'label': c, 'value': c} for c in unique_countries],
                                    value=unique_countries[:4],  # Default 4 negara pertama
                                    multi=True
                                )
                            ], md=6),
                        ]),
                        html.Label("Select Year Range", className="fw-bold mt-4"),
                        dcc.RangeSlider(
                            id='year-slider',
                            min=min_year,
                            max=max_year,
                            step=1,
                            marks={year: str(year) for year in range(min_year, max_year + 1, 2)},
                            value=[min_year, max_year]
                        )
                    ]),
                ),
                width=12,
                className="mb-4"
            )
        ),

        # Baris untuk Metrik Utama dan Grafik Tren
        dbc.Row([
            dbc.Col(dcc.Graph(id='time-series-plot'), lg=8),
            dbc.Col(html.Div(id='metrics-display'), lg=4, className="d-flex flex-column justify-content-center"),
        ], className="mb-4 align-items-center"),

        # Baris untuk Peta dan Grafik Perbandingan
        dbc.Row([
            dbc.Col(dcc.Graph(id='map-plot'), lg=7),
            dbc.Col(dcc.Graph(id='comparison-plot'), lg=5),
        ]),

        # Footer
        html.Footer(
            dbc.Row(
                dbc.Col(
                    html.P([
                        "Data Source: ", html.A("Pacific Data Hub (PDH.STAT)", href="https://stats.pacificdata.org/", target="_blank"),
                        " | Theme: ", html.A("2050 Strategy for the Blue Pacific Continent", href="https://www.forumsec.org/2050-strategy/", target="_blank")
                    ], className="text-center text-muted mt-5 py-3 border-top")
                )
            )
        )
    ])