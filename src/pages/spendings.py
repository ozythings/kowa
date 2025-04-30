from dash import html, dcc, dash_table, register_page
from utils.load_data import current_year, monthsToInt, load_categories, load_local_categories

register_page(__name__, "/spendings")

def spendings_layout(use_remote_db=False):
    if use_remote_db:
        categories_df = load_categories()
    else:
        categories_df = load_local_categories()

    return html.Div([

        dcc.Location(id="url"),
        dcc.Store(id="login_status", storage_type="local"),
        dcc.Store(id="signup_status", storage_type="local"),
        dcc.Store(id="signout_status", storage_type="local"),

        html.Div([
            html.H1("Financial Management", className="text-2xl md:text-4xl font-extrabold mb-4 text-gray-800"),
            html.P(
                'Enter your expenses and customize your budget categories on this page to keep your finances organized and under control.',
                className="font-medium text-gray-700 mb-6 md:mb-10 text-sm md:text-lg max-w-3xl"
            ),

            # Main content container - horizontal on desktop, vertical on mobile
            html.Div([
                # Left Section (Add Transaction + Monthly Budget)
                html.Div([
                    # Add Transaction Section
                    html.Div([
                        html.H2("Add Transaction", className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-blue-700"),
                        
                        html.Div([
                            html.H3("Select date", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.DatePickerSingle(
                                id='input_date',
                                placeholder='YYYY-MM-DD',
                                display_format='YYYY-MM-DD',
                                className="w-full"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Amount", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_amount',
                                type='number',
                                min=0,
                                placeholder='enter amount',
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Category", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id='input_category',
                                options=[{'label': category, 'value': category} for category in categories_df['name']],
                                placeholder='select category',
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Description", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_description',
                                type='text',
                                placeholder='enter description',
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Button('ADD', id='submit_transaction', n_clicks=0, 
                                  className="w-full py-2 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='transaction_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ], className="mb-8 md:mb-0"),
                    
                    # Monthly Budget Section
                    html.Div([
                        html.H2("Monthly Budget", className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-green-700"),
                        
                        html.Div([
                            html.H3("Month", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id="slct_budget_month",
                                options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                                multi=False,
                                placeholder='select month',
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Year", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id="slct_budget_year",
                                options=[{'label': year, 'value': year} for year in range(2023, (current_year() + 1) + 1)],
                                multi=False,
                                placeholder='select year',
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Budget", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='input_total_budget',
                                type='number',
                                min=0,
                                placeholder='enter budget',
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div(id='total_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600"),
                        html.Button('UPDATE', id='submit_total_budget', n_clicks=0, 
                                    className="w-full py-2 font-bold text-white bg-green-600 hover:bg-green-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='monthly_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ], className="mb-8 md:mb-0"),
                ], className="flex flex-col space-y-8 md:space-y-0 md:space-x-8 md:flex-row md:w-1/2"),
                
                # Vertical divider - hidden on mobile
                html.Div(className="hidden md:block border-l border-gray-300 mx-0 md:mx-4"),
                
                # Right Section (Category Budget + Budget Overview)
                html.Div([
                    # Category Budget Section
                    html.Div([
                        html.H2("Category Budget", className="text-xl md:text-2xl font-semibold mb-4 md:mb-6 text-purple-700"),
                        
                        html.Div([
                            html.H3("Category", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Dropdown(
                                id='budget_category_dropdown',
                                options=[{'label': category, 'value': category} for category in categories_df['name']],
                                placeholder='select category',
                                className="text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Div([
                            html.H3("Budget", className="text-xs md:text-sm font-medium text-gray-800 mb-1"),
                            dcc.Input(
                                id='budget_category_input',
                                type='number',
                                min=0,
                                placeholder='enter Budget',
                                className="w-full px-3 py-2 border border-gray-300 rounded text-xs md:text-sm"
                            )
                        ], className="w-full mb-4 md:mb-5"),
                        
                        html.Button('SET', id='submit_category_budget', n_clicks=0, 
                                   className="w-full py-2 font-bold text-white bg-purple-600 hover:bg-purple-700 rounded shadow text-sm md:text-base"),
                        html.Div(id='category_budget_status', className="mt-2 md:mt-3 text-xs md:text-sm text-gray-600")
                    ], className="mb-8"),
                    
                    # Budget Overview Section
                    html.Div([
                        html.H2("Budget Overview", className="text-xl md:text-2xl font-semibold mb-4 text-gray-800"),
                        dash_table.DataTable(
                            id='budget_table',
                            columns=[
                                {'name': 'Category', 'id': 'categoryname', 'type': 'text'},
                                {'name': 'Budget', 'id': 'categorybudget', 'type': 'numeric', 'editable': True}
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

layout = spendings_layout()
