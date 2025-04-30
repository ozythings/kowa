import dash
from dash import html, dcc


dash.register_page(__name__,"/temp")

layout = html.Div([
    html.Div("test", className="text-3xl")
])
