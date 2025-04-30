from dash import Dash, State, html, dcc, Output, Input
import dash
from flask import session
from flask_caching import Cache

def debug_callback(app):
    @app.callback(
        Output('test', 'children'),
        Input('url', 'pathname')
    )
    def test(_):
        return ""
