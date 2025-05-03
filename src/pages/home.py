import dash
from dash import html, dcc
from flask import session
from i18n.home_labels import get_home_labels

dash.register_page(__name__, path="/")

def home_layout(lang="en"):

    labels = get_home_labels(lang)

    if session.get("logged_in"):
        hero_btn = dcc.Link(labels["hero_btn_dashboard"], href=f"/dashboard?lang={lang}", className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700")
    else:
        hero_btn = dcc.Link(labels["hero_btn_signup"], href=f"/signup?lang={lang}", className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700")

    return html.Div([
        # hero
        html.Div([
            html.Div([
                html.Div([
                    html.H1(labels["hero_title"], className="text-4xl font-semibold mb-4"),
                    html.P(labels["hero_subtitle"], className="text-gray-600 mb-6"),
                    html.Div(hero_btn, id="hero-btn", className="mt-10")
                ], className="max-w-xl", id="hero"),
            ], className="flex justify-around items-center px-10")
        ], className="bg-gray-100 py-20"),

        # instructions
        html.Div([
            html.Div([
                html.Div([
                    html.H1(labels["how_kowa_works"], className="text-3xl font-bold text-center mb-8"),
                    html.Div([
                        html.Div([
                            html.Img(src='/assets/images/rocket.png', className='w-12 h-12 flex-shrink-0'),
                            html.Div([
                                html.H2(labels["get_started"], className='text-xl font-semibold'),
                                html.P(labels["get_started_desc"], className='text-gray-600')
                            ])
                        ], className='flex gap-4 items-start mb-6'),

                        html.Div([
                            html.Img(src='/assets/images/pencil.png', className='w-12 h-12 flex-shrink-0'),
                            html.Div([
                                html.H2(labels["monitor_spending"], className='text-xl font-semibold'),
                                html.P(labels["monitor_spending_desc"], className='text-gray-600')
                            ])
                        ], className='flex gap-4 items-start mb-6'),

                        html.Div([
                            html.Img(src='/assets/images/heart.png', className='w-12 h-12 flex-shrink-0'),
                            html.Div([
                                html.H2(labels["achieve_financial_peace"], className='text-xl font-semibold'),
                                html.P(labels["achieve_financial_peace_desc"], className='text-gray-600')
                            ])
                        ], className='flex gap-4 items-start mb-6'),
                    ], className='text-left')
                ], className='px-4 max-w-4xl mx-auto')
            ], className='py-20 bg-white')
        ]),

        # about
        html.Div([
            html.Div([
                html.H2(labels["about_creators"], className="text-2xl font-bold text-center mb-10"),
                html.Div([
                    html.Div([
                        html.H3(labels["creator_name"], className='text-xl font-semibold'),
                        html.P(labels["creator_desc"]),
                        html.Div([
                            dcc.Link(labels["creator_linkedin"], href='https://www.linkedin.com/in/hm', className='text-blue-500 underline mr-4', target='_blank'),
                            dcc.Link(labels["creator_github"], href='https://github.com/ozythings', className='text-blue-500 underline', target='_blank')
                        ], className='mt-2')
                    ], className='text-center')
                ], className='flex flex-col items-center mb-10')
            ], className='bg-gray-50 py-20')
        ]),

        # footer
        html.Div([
            html.Div([
                html.H1(labels["footer_title"], className='text-2xl font-bold'),
                html.H2(labels["footer_copyright"], className='text-sm')
            ], className='text-center mb-2'),
            html.Div([
                html.P(labels["footer_contact"], className='text-center text-gray-500')
            ])
        ], className='bg-black text-white py-10')
    ], className='font-sans')

# it expects page_args if its a function layout
def layout(**page_args):
    return home_layout(page_args.get("lang"))

