from urllib.parse import parse_qs, urlencode
from dash import Dash, State, html, dcc, Output, Input
import dash
from flask import session
from flask_caching import Cache

from i18n.navbar_labels import get_navbar_labels
from utils.url_helpers import get_lang_from_query

def navbar_callback(app):
    @app.callback(
        Output('navbar', 'children'),
        Input('url', 'pathname'),
        State('url', 'search')
    )
    def update_navbar(_, search):

        lang = get_lang_from_query(search) or "en"

        labels = get_navbar_labels(lang)
        logged_in = session.get("logged_in", False)

        nav_links = []

        # TODO: write a wrapper for language
        # use lang-store maybe?
        if logged_in:
            nav_links.extend([
                dcc.Dropdown(
                    id="language-selector",
                    options=[
                        {"label": "English", "value": "en"},
                        {"label": "Türkçe", "value": "tr"}
                    ],
                    value=None,
                    clearable=False,
                    style={"width": "150px"},
                    placeholder=labels["select_language"]
                ),
                dcc.Link(labels["dashboard"], href=f'/dashboard?lang={lang}', className='text-lg text-white hover:underline'),
                dcc.Link(labels["spendings"], href=f'/spendings?lang={lang}', className='text-lg text-white hover:underline'),
                dcc.Link(labels["upload"], href=f'/upload?lang={lang}', className='text-lg text-white hover:underline'),
                dcc.Link(labels["settings"], href=f'/settings?lang={lang}', className='text-lg text-white hover:underline'),
                html.Button(
                    labels["logout"],
                    id="logout_button",
                    className="px-4 py-2 bg-blue-700 text-white font-semibold rounded-lg hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                )
            ])
        else:
            nav_links.extend([
                dcc.Dropdown(
                    id="language-selector",
                    options=[
                        {"label": "English", "value": "en"},
                        {"label": "Türkçe", "value": "tr"}
                    ],
                    value=None,
                    clearable=False,
                    style={"width": "150px"},
                    placeholder=labels["select_language"]
                ),
                dcc.Link(labels["signin"], href=f'/signin?lang={lang}', className='text-lg text-white hover:underline'),
                dcc.Link(labels["signup"], href=f'/signup?lang={lang}', className='text-lg text-white hover:underline'),
            ])

        return html.Div([
            html.Div([
                html.Div([
                    dcc.Link(
                        html.H1(labels["app_name"], className='text-3xl font-bold text-white'),
                        href=f'/?lang={lang}',
                        className='flex-shrink-0'
                    ),
                    html.Button(
                        id='mobile-menu-button',
                        className='md:hidden flex flex-col justify-center items-center w-8 h-8',
                        children=[
                            html.Span(id='line1',className='block w-6 h-0.5 bg-white mb-1.5 transition-all duration-300'),
                            html.Span(id='line2',className='block w-6 h-0.5 bg-white mb-1.5 transition-all duration-300'),
                            html.Span(id='line3',className='block w-6 h-0.5 bg-white transition-all duration-300'),
                        ]
                    )
                ], className='flex justify-between items-center w-full md:w-auto'),
                html.Div(
                    id='mobile-menu',
                    className='hidden md:flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4 w-full md:w-auto mt-4 md:mt-0',
                    children=nav_links
                )
            ], className='flex flex-col md:flex-row justify-between items-center py-4 px-6 bg-gradient-to-r from-purple-600 to-blue-500 w-full')
        ])

        # @app.callback(
        #     Output("navbar","children"),
        #     Input("url","pathname")
        # )
        # def test():
        #     pass


    @app.callback(
        [Output('mobile-menu', 'className'),
         Output('line1', 'className'),
         Output('line2', 'className'),
         Output('line3', 'className')],
        Input('mobile-menu-button', 'n_clicks'),
        [State('mobile-menu', 'className'),
         State('line1', 'className'),
         State('line2', 'className'),
         State('line3', 'className')],
        prevent_initial_call=True
    )
    def toggle_mobile_menu(n_clicks, menu_class, line1_class, line2_class, line3_class):
        if n_clicks is None:
            return dash.no_update

        is_hidden = 'hidden' in menu_class

        new_menu_class = menu_class.replace('hidden', 'flex') if is_hidden else menu_class.replace('flex', 'hidden')

        if is_hidden:
            new_line1_class = line1_class + ' rotate-45 translate-y-2'
            new_line2_class = line2_class + ' opacity-0'
            new_line3_class = line3_class + ' -rotate-45 -translate-y-2'
        else:
            new_line1_class = line1_class.replace(' rotate-45 translate-y-2', '')
            new_line2_class = line2_class.replace(' opacity-0', '')
            new_line3_class = line3_class.replace(' -rotate-45 -translate-y-2', '')

        return new_menu_class, new_line1_class, new_line2_class, new_line3_class
