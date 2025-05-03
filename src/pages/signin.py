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
                html.Div([
                    html.Img(
                        src="/assets/images/question.png", 
                        className='w-64 h-64 mx-auto mb-8',
                        alt=labels["illustration_alt"]
                    ),

                    html.H1(
                        labels["title"],
                        className='text-3xl font-bold text-center mb-8 text-gray-800'
                    ),

                    dcc.Input(
                        id='login_email',
                        type='text',
                        placeholder=labels["username_placeholder"],
                        className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ),

                    dcc.Input(
                        id='login_password',
                        type='password',
                        placeholder=labels["password_placeholder"],
                        className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ),

                    html.Button(
                        labels["login_button"],
                        id='login_button',
                        className='w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors mb-4'
                    ),

                    html.Div(
                        id='login_message',
                        className='text-center text-red-500',
                        children=labels["login_message"]
                    )
                ], className='w-full max-w-md mx-auto')
            ], className='w-full max-w-2xl mx-auto bg-white p-8 md:p-12 rounded-lg shadow-md')
        ], className='flex justify-center items-center min-h-screen bg-gray-100 px-4')
    ], className='min-h-screen flex flex-col')

def layout(**page_args):
    return signin_layout(page_args.get("lang"))
