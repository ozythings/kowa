from urllib.parse import parse_qs
from dash import Input, Output, State
from dash.dash import urlparse

def get_lang_from_query(query_search):
    if query_search:
        from urllib.parse import parse_qs
        query_params = parse_qs(query_search[1:])
        lang = query_params.get('lang', ['en'])[0]
        return lang

def url_helper_callback(app):
    @app.callback(
        Output('url', 'href'),
        Input('lang-store', 'data'),
        State('url', 'pathname')
    )
    def update_url_with_lang(lang_data, pathname):
        lang = lang_data.get('lang', 'en')

        parsed_url = urlparse(pathname)
        query_params = parse_qs(parsed_url.query)
        query_params['lang'] = lang
        query = '&'.join([f"{key}={value[0]}" for key, value in query_params.items()])

        return f'{pathname}?{query}'
