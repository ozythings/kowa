from dash import html, dcc, dash_table, register_page
from flask import session
from i18n.dashboard_labels import get_category_labels
from i18n.spendings_labels import get_spendings_labels
from pages.unauthorized import unauthorized_layout
from utils.load_data import current_year, monthsToInt, load_categories, load_local_categories

register_page(__name__, "/spendings")

def spendings_layout(lang="en", use_remote_db=False):

    labels = get_spendings_labels(lang)
    category_labels = get_category_labels(lang)

    if use_remote_db:
        categories_df = load_categories()
    else:
        categories_df = load_local_categories()

    return html.Div([

        html.Div([
            html.H1(labels["financial_management"], className="text-2xl md:text-4xl font-extrabold mb-4 text-gray-800"),
            html.P(
                labels["top_info"],
                className="font-medium text-gray-700 mb-6 md:mb-10 text-sm md:text-lg max-w-3xl"
            ),

            html.Div([
                # left Section (add transaction + monthly budget)
                html.Div([
                    html.Div([
                        html.H2(labels["add_transaction"], className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-blue-700"),
                        html.Div([
                            html.H3(labels["select_date"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                    id="input_date",
                                    type="date", # this breaks down new dash versions
                                    className="w-full px-3 py-2 border border-gray-300 rounded text-sm"
                                ),
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["amount"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_amount',
                                type='number',
                                min=0,
                                placeholder=labels["enter_amount"],
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["category"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id='input_category',
                                options=[{'label': category_labels[category], 'value': category} for category in categories_df['name']],
                                placeholder=labels["select_category"],
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["description"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_description',
                                type='text',
                                placeholder=labels["enter_description"],
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),

                        html.Div([
                            html.H3(labels["installment"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Slider(
                                id='spendings-installment',
                                min=0,
                                max=24,
                                value=0,
                                marks={0: labels["no_installment"]},
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": False},
                                className="mb-4"
                            )
                        ], className="w-full mb-4 md:mb-5"),

                        html.Div(id='installment_value_display', className="text-xs md:text-sm text-gray-600 mt-2"),

                        html.Button(labels['add'], id='submit_transaction', n_clicks=0, 
                                  className="w-full py-2 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='transaction_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ], className="mb-8 md:mb-0"),
                    
                    html.Div([
                        html.H2(labels["monthly_budget"], className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-green-700"),
                        
                        html.Div([
                            html.H3(labels["month"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id="slct_budget_month",
                                options=[{'label': key, 'value': value} for key, value in monthsToInt(lang).items()],
                                multi=False,
                                placeholder=labels["select_month"],
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["year"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id="slct_budget_year",
                                options=[{'label': year, 'value': year} for year in range(2023, (current_year() + 1) + 1)],
                                multi=False,
                                placeholder=labels["select_year"],
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["budget"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_total_budget',
                                type='number',
                                min=0,
                                placeholder=labels["enter_budget"],
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div(id='total_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600"),
                        html.Button(labels["update"], id='submit_total_budget', n_clicks=0, 
                                    className="w-full py-2 font-bold text-white bg-green-600 hover:bg-green-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='monthly_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600"),
                    ], className="mb-8 md:mb-0"),
                ], className="flex flex-col space-y-8 md:space-y-0 md:space-x-8 md:flex-row md:w-1/2"),
                
                # vertical divider - hidden on mobile
                html.Div(className="hidden md:block border-l border-gray-300 mx-0 md:mx-4"),
                
                # right section (category budget + budget overview)
                html.Div([
                    html.Div([
                        html.H2(labels["category_budget"], className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-purple-700"),
                        
                        html.Div([
                            html.H3(labels["category"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id='budget_category_dropdown',
                                options=[{'label': category_labels[category], 'value': category} for category in categories_df['name']],
                                placeholder=labels["select_category"],
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3(labels["budget"], className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='budget_category_input',
                                type='number',
                                min=0,
                                placeholder=labels["enter_budget"],
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Button(labels["set"], id='submit_category_budget', n_clicks=0, 
                                   className="w-full py-2 font-bold text-white bg-purple-600 hover:bg-purple-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='category_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ], className="mb-8"),
                    
                    html.Div([
                        html.H2(labels["budget_overview"], className="text-xl md:text-2xl font-semibold mb-4 text-gray-800"),
                        dash_table.DataTable(
                            id='budget_table',
                            columns=[
                                {'name': labels["category"], 'id': 'categoryname', 'type': 'text'},
                                {'name': labels["budget"], 'id': 'categorybudget', 'type': 'numeric', 'editable': True}
                            ],
                            data=[],
                            style_table={'overflowX': 'auto', 'minWidth': '100%'},
                            style_cell={
                                'fontFamily': 'Arial', 
                                'fontSize': '12px',
                                'minWidth': '80px', 'maxWidth': '150px',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                            },
                            style_header={
                                'fontWeight': 'bold', 
                                'backgroundColor': '#f4f4f4',
                                'fontSize': '12px'
                            }
                        ),
                        html.Div(id='budget_overview_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ]),
                ], className="md:w-1/2"),
                
                html.Div(id='update_trigger', style={'display': 'none'}),
            ], className="flex flex-col md:flex-row bg-white rounded-xl p-6 md:p-10 shadow-[0_0_60px_1px_rgba(0,0,0,0.1)] w-full")
        ], className="w-full max-w-6xl rounded-lg flex flex-col items-center justify-center p-4 md:p-8 text-left bg-[#f9fafb] border border-gray-200 shadow-md mx-2 md:mx-8 my-4 md:my-8")
    ], className="min-h-screen w-full overflow-auto flex justify-center items-center")

def layout(**page_args):
    if session.get("logged_in"):
        return spendings_layout(page_args.get("lang"))
    else:
        return unauthorized_layout(page_args.get("lang"))
