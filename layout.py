from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout(indicators, countries):
    return html.Div([
        # Header
        dbc.Navbar(
            dbc.Container([
                html.A(
                    dbc.Row([
                        dbc.Col(html.Img(src="/assets/logo.png", height="40px")),
                        dbc.Col(dbc.NavbarBrand("Blue Pacific 2050 Dashboard", className="ms-2")),
                    ], align="center", className="g-0"),
                    href="#",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            ]),
            color="primary",
            dark=True,
        ),

        # Konten utama
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3("Technology & Connectivity in the Pacific", className="mt-4"),
                    html.P("Visualizing progress toward the Blue Pacific 2050 goals", className="text-muted"),

                    # Kontrol filter
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Select Indicator:"),
                                    dcc.Dropdown(
                                        id='indicator-selector',
                                        options=[{'label': i, 'value': i} for i in indicators],
                                        value='Proportion of individuals using the Internet',
                                        clearable=False
                                    )
                                ], md=4),
                                dbc.Col([
                                    html.Label("Select Countries:"),
                                    dcc.Dropdown(
                                        id='country-selector',
                                        options=[{'label': i, 'value': i} for i in countries],
                                        value=['Cook Islands', 'Samoa', 'Fiji'],
                                        multi=True
                                    )
                                ], md=4),
                                dbc.Col([
                                    html.Label("Year Range:"),
                                    dcc.RangeSlider(
                                        id='year-slider',
                                        min=2000,
                                        max=2024,
                                        step=1,
                                        marks={year: str(year) for year in range(2000, 2025, 5)},
                                        value=[2010, 2020],
                                        tooltip={"placement": "bottom", "always_visible": True}
                                    )
                                ], md=4),
                            ])
                        ])
                    ], className="mb-4"),

                    # Grafik
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='time-series-plot'), md=6),
                        dbc.Col(dcc.Graph(id='comparison-plot'), md=6),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='demographic-plot'), md=12),
                    ]),
                ])
            ]),

            # Footer
            dbc.Row([
                dbc.Col(html.Div([
                    html.Hr(),
                    html.P([
                        "Data Source: ",
                        html.A("Pacific Data Hub", href="https://stats.pacificdata.org/", target="_blank"),
                        " | Blue Pacific 2050 Strategy"
                    ], className="text-center text-muted")
                ]), md=12)
            ])
        ], fluid=True)
    ])