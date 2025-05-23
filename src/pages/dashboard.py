from dash import html, dcc, dash_table, register_page
from flask import session
import pandas as pd
from i18n.dashboard_labels import get_category_labels, get_correct_category_labels, get_dashboard_labels
from pages.unauthorized import unauthorized_layout
from utils.load_data import current_month, current_year, load_categories, load_local_categories, monthsToInt, load_transactions, load_local_transactions

register_page(__name__, path='/dashboard', name='Dashboard', title='Budget Dashboard')

def dashboard_layout(lang="en", use_remote_db=False):
    
    labels = get_dashboard_labels(lang)

    if use_remote_db:
        transactions = load_transactions()
        categories_df = load_categories()
    else:
        transactions = load_local_transactions()
        categories_df = load_local_categories()

    transactions['date'] = pd.to_datetime(transactions['date'])
    transactions['date_display'] = transactions['date'].dt.strftime('%Y-%m-%d')
    transactions.sort_values('date', ascending=False, inplace=True)  # Sort by date descending

    category_labels = get_category_labels(lang)
    transactions_tr = transactions.copy()
    transactions_tr['categoryname'] = transactions_tr['categoryname'].map(category_labels)
    transactions_tr['date_display'] = pd.to_datetime(transactions_tr['date']).dt.strftime('%Y-%m-%d')

    print("--------------------\n", transactions_tr)


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
                html.H1(labels["year_month_title"], className="text-xl font-bold mb-4"),
                html.Div([
                    html.H2(labels["select_year"], className="text-lg font-medium mb-2"),
                    dcc.Dropdown(
                        id="slct_year",
                        options=[
                            {'label': str(year), 'value': year} for year in range(current_year()-2, current_year()+3)
                        ],
                        multi=False,
                        value=last_transaction_year,
                        placeholder=labels["select_year"],
                        className='w-full mb-4',
                    ),
                ], className='mb-4'),
                html.Div([
                    html.H2(labels["select_month"], className="text-lg font-medium mb-2"),
                    dcc.Dropdown(
                        id="slct_month",
                        options=[{'label': key, 'value': value} for key, value in monthsToInt(lang).items()],
                        multi=False,
                        value=current_month(),
                        placeholder=labels["select_month"],
                        className='w-full',
                    )
                ])
            ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

            html.Div([
                html.H1(labels["net_balance_title"], className="text-xl font-bold mb-2"),
                html.P(id='net-balance-output', className='p-4 bg-gray-100 rounded-md text-lg mb-4'),
                html.H1(labels["performance_title"], className="text-xl font-bold mb-2"),
                html.P(id='status-output', className='p-4 bg-gray-100 rounded-md text-lg')
            ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

            html.Div([
                html.H1(labels["expense_categorization_title"], className="text-xl font-bold mb-4"),
                dcc.Graph(id='expense_categorization_graph', figure={}),
            ], className='bg-white p-6 rounded-lg shadow-md')
        ], className='w-1/3 pr-4'),

        html.Div([
            html.Div([
                html.Div([
                    html.H1(labels["daily_spending_title"], className="text-xl font-bold mb-4"),
                    dcc.Graph(id='daily_spending_trend_graph', figure={}, className="placeholder-black"),
                ], className='bg-white p-6 rounded-lg shadow-md mb-6'),

                html.Div([
                    html.H1(labels["budget_vs_spending_title"], className="text-xl font-bold mb-4"),
                    dcc.Graph(id='budget_vs_actual_spending_graph', figure={}),
                ], className='bg-white p-6 rounded-lg shadow-md'),
            ], className='mb-6'),

            html.Div([
                html.H1(labels["recent_transactions_title"], className="text-xl font-bold mb-4"),
                dash_table.DataTable(
                    id='transactions_table',
                    columns=[
                        {"name": labels["table_headers"]["date"], "id": "date_display"},
                        {"name": labels["table_headers"]["category"], "id": "categoryname"},
                        {"name": labels["table_headers"]["amount"], "id": "amount"},
                        {"name": labels["table_headers"]["description"], "id": "description"}
                    ],
                    data=transactions_tr.to_dict('records'),
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

def categories_from_records(records, lang="en"):
    category_mapping = get_category_labels(lang)
    
    for row in records:
        original_name = row['categoryname']
        row['categoryname'] = category_mapping.get(original_name, original_name)

    return records

def layout(**page_args):
    if session.get("logged_in"):
        return dashboard_layout(page_args.get("lang"))
    else:
        return unauthorized_layout(page_args.get("lang"))
