import dash
from dash import html, dcc
from flask import session

dash.register_page(__name__, path="/")

def home_layout():
    return html.Div([
    dcc.Location(id="url"),
    # hero
    html.Div([
        html.Div([
            html.Div([
                html.H1("Visualize Your Finances", className="text-4xl font-semibold mb-4"),
                html.P("Gain control over your expenses. Discover clear, visual insights into your spending to help you budget smarter and save more.", className="text-gray-600 mb-6"),
                html.Div(id="hero-btn", className="mt-10")
            ], className="max-w-xl", id="hero"),
            #html.Img(src="/assets/images/logo.png", className="w-40")
        ], className="flex justify-around items-center px-10")
    ], className="bg-gray-100 py-20"),

    # instructions
    html.Div([
        html.Div([
            html.Div([
                html.H1("How kowa works", className="text-3xl font-bold text-center mb-8"),

                html.Div([
                    html.Div([
                        html.Img(src='/assets/images/rocket.png', className='w-12 h-12 flex-shrink-0'),
                        html.Div([
                            html.H2('Get Started Easily', className='text-xl font-semibold'),
                            html.P('Sign up quickly with no credit card required and start managing your finances immediately.', className='text-gray-600')
                        ])
                    ], className='flex gap-4 items-start mb-6'),

                    html.Div([
                        html.Img(src='/assets/images/pencil.png', className='w-12 h-12 flex-shrink-0'),
                        html.Div([
                            html.H2('Monitor Your Spending', className='text-xl font-semibold'),
                            html.P('Enter your expenses and view an updated dashboard to help plan and save effectively.', className='text-gray-600')
                        ])
                    ], className='flex gap-4 items-start mb-6'),

                    html.Div([
                        html.Img(src='/assets/images/heart.png', className='w-12 h-12 flex-shrink-0'),
                        html.Div([
                            html.H2('Achieve Financial Peace', className='text-xl font-semibold'),
                            html.P('Stay informed with real-time updates and visual data, reducing stress and boosting confidence.', className='text-gray-600')
                        ])
                    ], className='flex gap-4 items-start mb-6'),
                ], className='text-left')
            ], className='px-4 max-w-4xl mx-auto')
        ], className='py-20 bg-white')
    ]),
    # about
    html.Div([
        html.Div([
            html.H2("About The Creators", className="text-2xl font-bold text-center mb-10"),

            html.Div([
                html.Div([
                    html.H3('ozy', className='text-xl font-semibold'),
                    html.P('Computer Engineering Student @ Amasya University'),
                    html.Div([
                        dcc.Link('LinkedIn', href='https://www.linkedin.com/in/hm', className='text-blue-500 underline mr-4', target='_blank'),
                        dcc.Link('Github', href='https://github.com/ozythings', className='text-blue-500 underline', target='_blank')
                    ], className='mt-2')
                ], className='text-center')
            ], className='flex flex-col items-center mb-10'),

            html.Div([
                html.Div([
                    html.H3('ozy', className='text-xl font-semibold'),
                    html.P('Computer Engineering Student @ Amasya University'),
                    html.Div([
                        dcc.Link('LinkedIn', href='https://www.linkedin.com/in/hm', className='text-blue-500 underline mr-4', target='_blank'),
                        dcc.Link('Github', href='https://github.com/ozythings', className='text-blue-500 underline', target='_blank')
                    ], className='mt-2')
                ], className='text-center')
            ], className='flex flex-col items-center mb-10'),
        ], className='bg-gray-50 py-20')
    ]),

    # footer
    html.Div([
        html.Div([
            html.H1('kowa', className='text-2xl font-bold'),
            html.H2('Copyright © 2025, kowa. All Rights Reserved.', className='text-sm')
        ], className='text-center mb-2'),
        html.Div([
            html.P('ozythings', className='text-center text-gray-500')
        ])
    ], className='bg-black text-white py-10')
], className='font-sans')

layout = home_layout()
