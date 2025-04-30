from dash import html, dcc
from dash import Input, Output, State, callback
import dash
from sqlalchemy.engine.reflection import cache
from flask_caching import Cache
from flask import session

def navbar():
    return html.Div(id="navbar")
