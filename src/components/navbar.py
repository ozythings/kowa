from dash import html, dcc
from dash import Input, Output, State, callback
import dash
from sqlalchemy.engine.reflection import cache
from flask_caching import Cache
from flask import session

def navbar():
    return html.Div([
        html.Div([
            dcc.Store(id={"type": "storage", "index": "local"}),
            # Logo and hamburger button
            html.Div([
                dcc.Link(
                    html.H1("kowa", className='text-3xl font-bold text-white'),
                    href='/',
                    className='flex-shrink-0'
                ),
                # Hamburger button (visible only on mobile)
                html.Button(
                    id='mobile-menu-button',
                    className='md:hidden flex flex-col justify-center items-center w-8 h-8',
                    children=[
                        html.Span(className='block w-6 h-0.5 bg-white mb-1.5 transition-all duration-300', id='line1'),
                        html.Span(className='block w-6 h-0.5 bg-white mb-1.5 transition-all duration-300', id='line2'),
                        html.Span(className='block w-6 h-0.5 bg-white transition-all duration-300', id='line3'),
                    ]
                )
            ], className='flex justify-between items-center w-full md:w-auto'),
            
            # Navigation links (hidden on mobile by default)
            html.Div(
                id='mobile-menu',
                className='hidden md:flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4 w-full md:w-auto mt-4 md:mt-0',
                children=[
                    dcc.Link("Dashboard",
                        href='/dashboard',
                        className='text-lg text-white hover:underline w-full text-center md:w-auto md:text-left'
                    ),

                    dcc.Link("Spendings",
                        href='/spendings',
                        className='text-lg text-white hover:underline w-full text-center md:w-auto md:text-left'
                    ),
                ]
            )
        ], className='flex flex-col md:flex-row justify-between items-center py-4 px-6 bg-gradient-to-r from-purple-600 to-blue-500 w-full')
    ])

@callback(
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
    
    if 'hidden' in menu_class:
        # Open menu
        new_menu_class = menu_class.replace('hidden', 'flex')
        new_line1_class = line1_class + ' rotate-45 translate-y-2'
        new_line2_class = line1_class + ' opacity-0'
        new_line3_class = line1_class + ' -rotate-45 -translate-y-2'
    else:
        # Close menu
        new_menu_class = menu_class.replace('flex', 'hidden')
        new_line1_class = line1_class.replace(' rotate-45 translate-y-2', '')
        new_line2_class = line2_class.replace(' opacity-0', '')
        new_line3_class = line3_class.replace(' -rotate-45 -translate-y-2', '')
    
    return new_menu_class, new_line1_class, new_line2_class, new_line3_class
