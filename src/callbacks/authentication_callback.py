from time import sleep
from typing import Dict
from dash import Input, Output, State, html, no_update
from flask import session
from i18n.signin_labels import get_signin_callback_labels
from i18n.signup_labels import get_signup_callback_labels
from utils.url_helpers import get_lang_from_query
from utils.user_management import create_local_user, validate_local_user, create_remote_user, validate_remote_user, email_exists_local, email_exists_remote

def authentication_callback(app, use_remote_db=False):
    @app.callback(
        [Output('login_status', 'data'),
         Output("login_message", "children")],
        Input('login_button', 'n_clicks'),
        State('login_email', 'value'),
        State('login_password', 'value'),
        State('url', 'search'),
        prevent_initial_call=True
    )
    def login_user(n_clicks, email, password, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_signin_callback_labels(lang)

        # check if email or password is missing
        if not email or not password:
            login_status = {'logged_in': False}
            login_message = html.Div(labels["please_enter_email_password"], className="text-red-500 mt-2 text-center")
            return login_status, login_message

        # validate user credentials
        if use_remote_db:
            userid = validate_remote_user(email, password)
        else:
            userid = validate_local_user(email, password)

        # ff user is authenticated, set session data
        if userid:
            # store login information in Flask session
            session["logged_in"] = True
            session["user_id"] = userid
            session["user_email"] = email
            session.permanent = True
            
            login_status = {
                'logged_in': True,
                'user_id': userid,
                'user_email': email,
            }
            login_message = html.Div(labels["login_successful"], className="text-green-500 mt-2 text-center")
        else:
            session.clear()
            login_status = {'logged_in': False}
            login_message = html.Div(labels["invalid_email_password"], className="text-red-500 mt-2 text-center")
        
        return login_status, login_message

    @app.callback(
        Output('signup_status', 'children'),
        [Input('signup_button', 'n_clicks')],
        [State('signup_name', 'value'), 
         State('signup_email', 'value'), 
         State('signup_password', 'value'), 
         State('signup_confirm_password', 'value'),
        State('url', 'search')],
    )
    def signup_user(n_clicks, name, email, password, confirm_password,search):

        lang = get_lang_from_query(search) or "en"
        labels = get_signup_callback_labels(lang)
        print(labels)
        if n_clicks:
            print("Signing up...", name, email)

            if name and email and password and confirm_password:
                if password != confirm_password:
                    return labels["password_mismatch"]
            
                if use_remote_db:
                    if email_exists_remote(email):
                        return labels["email_exists"]
                    create_remote_user(name, email, password)
                else:
                    if email_exists_local(email):
                        return labels["email_exists"]
                    create_local_user(name, email, password)
                
                login_user(1, email, password,search)
                return labels["account_created"]
            
            return labels["fill_out_fields"]
        return ''
   
    @app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input('login_button', 'n_clicks'),
        Input('login_status', 'data'),
        prevent_initial_call=True
    )
    def redirect_user(n_clicks, login_status):
        if n_clicks:
            if login_status and login_status.get("logged_in"):
                sleep(1)
                return '/dashboard'
        return no_update

    @app.callback(
        Output('url', 'pathname',allow_duplicate=True),
        Input('logout_button', 'n_clicks'),
        prevent_initial_call=True
    )
    def logout_user(n_clicks):
        if n_clicks:
            session.clear()
            sleep(1)
            return '/'
        return no_update
