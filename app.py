import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

# Inisialisasi aplikasi
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], use_pages=True)
server = app.server

# Navbar untuk navigasi
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Halaman Cerita", href=dash.page_registry['pages.narrative']['path'])),
        dbc.NavItem(dbc.NavLink("Dasbor Eksplorasi", href=dash.page_registry['pages.dashboard']['path'])),
    ],
    brand="Blue Pacific Data Challenge",
    brand_href=dash.page_registry['pages.narrative']['path'],
    color="primary",
    dark=True,
    className="mb-4"
)

# Layout utama aplikasi
app.layout = html.Div([
    navbar,
    # Konten halaman akan ditampilkan di sini
    dash.page_container
])


# Jalankan server
if __name__ == '__main__':
    app.run(debug=True)