from datetime import timedelta
import os
import dash
from dash import dcc, html
from flask import Flask
from utils.load_data import cache, test_connection
from utils.register_callbacks import register_callbacks
from components import navbar

server = Flask(__name__)
server.secret_key = os.getenv('SECRET_KEY')
server.config['SESSION_PERMANENT'] = True
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # session lifetime

# initializing caching for server
cache.init_app(server)

app = dash.Dash(__name__, server = server, use_pages= True, suppress_callback_exceptions=True) # type: ignore
app.title = "kowa"


app.layout = html.Div([
    dcc.Store("login_status"),
    dcc.Store(id='lang-store'),
    dcc.Location(id="url"),
    navbar(lang="en"),
    dash.page_container
])

try:
    register_callbacks(app, use_remote_db=False)
except Exception as e:
    print("Callback error:",e)

if __name__ == '__main__':
    #test_connection()
    app.run_server(debug=True, port=8051)
