from dash import html, dcc, register_page

from i18n.signup_labels import get_signup_labels

register_page(__name__, "/signup")

def signup_layout(lang="en"):
    labels = get_signup_labels(lang)

    return html.Div([
        html.Div([
            html.Div([
                html.Img(src="/assets/images/heart.png", 
                         className='w-64 h-64 mx-auto mb-8',
                         alt=labels["illustration_alt"]),
                
                html.H1(labels["title"], className='text-3xl font-bold text-center mb-8 text-gray-800'),
                
                html.Div([
                    dcc.Input(id='signup_name', 
                             type='text', 
                             placeholder=labels["name_placeholder"],
                             className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    dcc.Input(id='signup_email', 
                             type='email', 
                             placeholder=labels["email_placeholder"],
                             className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    dcc.Input(id='signup_password', 
                             type='password', 
                             placeholder=labels["password_placeholder"],
                             className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    dcc.Input(id='signup_confirm_password', 
                             type='password', 
                             placeholder=labels["confirm_password_placeholder"],
                             className='w-full px-4 py-3 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    html.Div(id='signup_status',
                             className='text-center text-red-500 mb-4')
                ], className='w-full max-w-md mx-auto'),
                
                html.Div([
                    html.Button(labels["register_button"], 
                               id='signup_button', 
                               className='w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition-colors mb-4'),
                    
                    html.Div([
                        html.Span(labels["already_have_account"], className='text-gray-600'),
                        dcc.Link(labels["signin_link"], 
                                 href=f'/signin?lang={lang}', 
                                 className='text-blue-600 hover:underline')
                    ], className='text-center')
                ], className='w-full max-w-md mx-auto')
            ], className='w-full max-w-2xl mx-auto bg-white p-8 md:p-12 rounded-lg shadow-md')
        ], className='flex-1 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50')
    ], className='min-h-screen flex flex-col')

def layout(**page_args):
    return signup_layout(page_args.get("lang"))

