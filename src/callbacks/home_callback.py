from dash import Input, Output, html, dcc
from flask import session

# this uses the dash dynamic thingy
# but i've used flask's session on dashboard
# i will probably update this
def home_callback(app):
    @app.callback(
        Output("hero-btn","children"),
        Input("url","pathname")
    )
    def hero_callback(pathname):
        if pathname == "/":
            if session.get("logged_in"):
                return dcc.Link("Dashboard", href="/dashboard", className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700")

            else:
                return dcc.Link("Sign up now", href="/signup", className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700")
        return html.Div()




