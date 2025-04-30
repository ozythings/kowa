from dash import html, dcc, register_page
from flask import session

from pages.unauthorized import unauthorized_layout

register_page(__name__, "/support")

def support_layout():
    return html.Div([
        html.Div([
            html.Div([    
                html.H1('Contact Form', className='text-3xl font-bold text-gray-800 mb-2'),
                html.P('Please fill out the form below to contact us. We will get back to you as soon as possible', 
                  className='text-gray-600 mb-8'),
                html.Div([
                    html.H2('Name', className='text-lg font-medium text-gray-700 mb-1'),
                    dcc.Input(
                        id='name-input',
                        type='text',
                        placeholder='your name',
                        className='w-full px-4 py-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ),
                    html.H2('Email', className='text-lg font-medium text-gray-700 mb-1'),
                    dcc.Input(
                        id='email-input',
                        type='email',
                        placeholder='your email',
                        className='w-full px-4 py-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500'
                    ),
                ], className='mb-6'),
                
                html.H2('Message to Creators', className='text-lg font-medium text-gray-700 mb-1'),
                dcc.Textarea(
                    id='message-input',
                    placeholder='Enter your message here',
                    className='w-full px-4 py-2 border border-gray-300 rounded-md mb-6 h-32 focus:outline-none focus:ring-2 focus:ring-blue-500'
                ),
                
                html.Div([
                    html.Button(
                        'SEND', 
                        id='support-send-button', 
                        n_clicks=0,
                        className='w-full md:w-auto px-6 py-3 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
                    ),
                ], className='relative'),
                
                html.Div(id='support-status', className='mt-4 text-sm')
            ], className='max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md')
        ], className='min-h-screen py-12 px-4 sm:px-6 lg:px-8 bg-gray-50')
    ])

def layout():
    if session.get("logged_in"):
        return support_layout()
    else:
        return unauthorized_layout()
