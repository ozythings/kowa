import dash
from dash import html, dcc
from components import navbar

dash.register_page(__name__, path="/signin")

def signin_layout():
    return html.Div([
        # Sign-in form container
        dcc.Store("login_status"),
        dcc.Store("login_message"),
        html.Div([
            html.Div([
                html.Img(src="/assets/images/question.png", 
                         className='w-64 h-64 mx-auto mb-8',
                         alt='illustration'),
                    
                html.H1(
                    "Sign In",
                    className='text-3xl font-semibold mb-6 text-center'
                ),
                html.Div([
                    dcc.Input(
                        id='login_email',
                        type='text',
                        placeholder='Username',
                        className='w-full mb-4 px-4 py-2 border rounded focus:outline-none focus:ring'
                    ),
                    dcc.Input(
                        id='login_password',
                        type='password',
                        placeholder='Password',
                        className='w-full mb-4 px-4 py-2 border rounded focus:outline-none focus:ring'
                    ),
                    html.Button(
                        'Login',
                        id='login_button',
                        className='w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600'
                    ),
                    html.Div(id='login_message')
                ], className='bg-white p-8 rounded-lg shadow-lg')
            ], className='max-w-md w-full')
        ], className='flex justify-center items-center min-h-screen bg-gray-100 px-4')
    ], className='font-sans')

layout = signin_layout()
