from dash import html, dcc, dash_table, register_page
from flask import session
import pandas as pd
from pages.unauthorized import unauthorized_layout
from utils.load_data import current_month, current_year, monthsToInt, load_transactions, load_local_transactions

register_page(__name__, path='/dashboard', name='Dashboard', title='Budget Dashboard')

def dashboard_layout(use_remote_db=False):
    if use_remote_db:
        transactions = load_transactions()
    else:
        transactions = load_local_transactions()

    transactions['date'] = pd.to_datetime(transactions['date'])
    transactions['date_display'] = transactions['date'].dt.strftime('%Y-%m-%d')
    transactions.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

    # find the last transaction date to set the default year and month
    if not transactions.empty:
        last_transaction_date = transactions['date'].iloc[0]
        last_transaction_year = last_transaction_date.year
        last_transaction_month = last_transaction_date.month
    else:
        last_transaction_year = current_year()
        last_transaction_month = current_month()

    return html.Div([
        html.Div([
            html.Div([
                html.H1("Year and Month", className="text-xl font-bold mb-4"),
                html.Div([
                    html.H2('Select year:', className="text-lg font-medium mb-2"),
                    dcc.Dropdown(
                        id="slct_year",
                        options=[
                            {'label': str(year), 'value': year} for year in range(2023, (current_year()+1)+1)
                        ],
                        multi=False,
                        value=last_transaction_year,
                        placeholder="Select year",
                        className='w-full mb-4',
                    ),
                ], className='mb-4'),
                html.Div([
                    html.H2('Select month:', className="text-lg font-medium mb-2"),
                    dcc.Dropdown(
                        id="slct_month",
                        options=[{'label': key, 'value': value} for key, value in monthsToInt().items()],
                        multi=False,
                        value=last_transaction_month,
                        placeholder="Select month",
                        className='w-full',
                    )
                ])
            ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

            html.Div([
                html.H1("Net Balance", className="text-xl font-bold mb-2"),
                html.P(id='net-balance-output', className='p-4 bg-gray-100 rounded-md text-lg mb-4'),
                html.H1("Performance", className="text-xl font-bold mb-2"),
                html.P(id='status-output', className='p-4 bg-gray-100 rounded-md text-lg')
            ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

            html.Div([
                html.H1("Expense Categorization", className="text-xl font-bold mb-4"),
                dcc.Graph(id='expense_categorization_graph', figure={}),
            ], className='bg-white p-6 rounded-lg shadow-md')
        ], className='w-1/3 pr-4'),

        html.Div([
            html.Div([
                html.Div([
                    html.H1("Daily Spending Trend", className="text-xl font-bold mb-4"),
                    dcc.Graph(id='daily_spending_trend_graph', figure={}, className="placeholder-black"),
                ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

                html.Div([
                    html.H1("Budget vs. Spending Per Category", className="text-xl font-bold mb-4"),
                    dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                ], className='bg-white p-6 rounded-lg shadow-md'),
            ], className='mb-6'),

            html.Div([
                html.H1("Recent Transactions", className="text-xl font-bold mb-4"),
                dash_table.DataTable(
                    id='transactions_table',
                    columns=[
                        {"name": "Date", "id": "date_display"},
                        {"name": "Category Name", "id": "categoryname"},
                        {"name": "Amount", "id": "amount"},
                        {"name": "Description", "id": "description"}
                    ],
                    data=transactions.to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'padding': '12px',
                        'textAlign': 'left'
                    },
                    style_header={
                        'backgroundColor': 'rgb(240, 240, 240)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 250, 252)'
                        }
                    ]
                )
            ], className='bg-white p-6 rounded-lg shadow-md')
        ], className='w-2/3')
    ], className='flex flex-wrap p-6 bg-gray-50')

def layout():
    if session.get("logged_in"):
        return dashboard_layout()
    else:
        return unauthorized_layout()

