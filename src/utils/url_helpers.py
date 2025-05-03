from urllib.parse import parse_qs, urlencode
from dash import Input, Output, State
import dash
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
        Input('language-selector', 'value'),  # ✅ Use dropdown directly
        State('url', 'pathname'),
        State('url', 'search'),
        prevent_initial_call=True  # optional: avoid redirect on first load
    )
    def update_url_with_lang(selected_lang, pathname, search):
        if not selected_lang:
            raise dash.exceptions.PreventUpdate

        query = parse_qs(search.lstrip("?"))
        query["lang"] = [selected_lang]
        updated_query = urlencode(query, doseq=True)

        return f"{pathname}?{updated_query}"
