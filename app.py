from dash import Dash
from data_loader import load_and_preprocess_data
from layout import create_layout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc

# Inisialisasi aplikasi
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           assets_folder='assets',
           suppress_callback_exceptions=True)
server = app.server

# Load data
data = load_and_preprocess_data('Blue Pacific 2050_ Technology And Connectivity (Thematic Area 7) data.csv')

# Setup layout
indicators = sorted(data['Indicator'].unique())
countries = sorted(data['Country'].unique())
app.layout = create_layout(indicators, countries)

# Register callbacks
register_callbacks(app, data)

# Jalankan aplikasi
if __name__ == '__main__':
    app.run_server(debug=True)