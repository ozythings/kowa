from callbacks import dashboard_callback, spendings_callback, authentication_callback, settings_callback, support_callback, home_callback
from callbacks import navbar_callback
from callbacks import debug_callback
from callbacks import upload_callback
from utils.url_helpers import url_helper_callback

def register_callbacks(app, use_remote_db):
    authentication_callback(app, use_remote_db)
    dashboard_callback(app, use_remote_db)
    spendings_callback(app, use_remote_db)
    settings_callback(app, use_remote_db)
    support_callback(app)
    home_callback(app)
    navbar_callback(app) 
    debug_callback(app)
    upload_callback(app)
    url_helper_callback(app)
