import dash
from dash import html, dcc
from components import navbar
from i18n.signin_labels import get_signin_labels

dash.register_page(__name__, path="/signin")

def signin_layout(lang="en"):
    labels = get_signin_labels(lang)

    return html.Div([

        dcc.Store("login_message"),

        html.Div([
            html.Div([
                html.Img(src="/assets/images/question.png", 
                         className='w-64 h-64 mx-auto mb-8',
                         alt=labels["illustration_alt"]),

                html.H1(
                    labels["title"],
                    className='text-3xl font-semibold mb-6 text-center'
                ),
                html.Div([
                    dcc.Input(
                        id='login_email',
                        type='text',
                        placeholder=labels["username_placeholder"],
                        className='w-full mb-4 px-4 py-2 border rounded focus:outline-none focus:ring'
                    ),
                    dcc.Input(
                        id='login_password',
                        type='password',
                        placeholder=labels["password_placeholder"],
                        className='w-full mb-4 px-4 py-2 border rounded focus:outline-none focus:ring'
                    ),
                    html.Button(
                        labels["login_button"],
                        id='login_button',
                        className='w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600'
                    ),
                    html.Div(id='login_message', children=labels["login_message"])
                ], className='bg-white p-8 rounded-lg shadow-lg')
            ], className='max-w-md w-full')
        ], className='flex justify-center items-center min-h-screen bg-gray-100 px-4')
    ], className='font-sans')

def layout(**page_args):
    return signin_layout(page_args.get("lang"))
