from dash import State, html, Input, Output
import pandas as pd
import plotly.express as px
from utils.load_data import userid, load_database, cache
from utils.url_helpers import get_lang_from_query
from i18n.dashboard_labels import get_category_labels, get_correct_category_labels, get_dashboard_callback_labels, get_dashboard_labels

def dashboard_callback(app, use_remote_db=False):

    @app.callback(
        [Output('net-balance-output', 'children'), 
        Output('status-output', 'children'),
        Output('expense_categorization_graph', 'figure'), 
        Output('daily_spending_trend_graph', 'figure'),
        Output('budget_vs_actual_spending_graph', 'figure'),
        Output('transactions_table', 'data')],

        [Input('slct_year', 'value'),
        Input('slct_month', 'value')],
        State("url","search")
    )
    #@cache.memoize()
    def update_graph(selected_year, selected_month, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_dashboard_callback_labels(lang)
        category_labels = get_category_labels(lang)

        # load data from the database
        transactions, monthly_budgets, categorical_budgets = load_database(use_remote_db)

        # filters to only include rows where the year and month match the input year and month for the logged-in user
        # boolean indexing: [ ] filters rows based on a condition
        filtered = transactions[(transactions['userid'] == userid()) &
                                    (transactions['date'].dt.year == selected_year) &
                                    (transactions['date'].dt.month == selected_month)]

        filtered['categoryname'] = filtered['categoryname'].map(category_labels)

        # ensure the dataframe is not empty
        if filtered.empty:
            return labels["no_transaction"], '', {}, {}, {}, []

        # total spent in a month
        total_spent = filtered['amount'].sum()

        # converting to date-time
        monthly_budgets['budgetmonth'] = pd.to_datetime(monthly_budgets['budgetmonth'])

        monthly_budget = monthly_budgets[
            (monthly_budgets['userid'] == userid()) &
            (monthly_budgets['budgetmonth'].dt.year == selected_year) &
            (monthly_budgets['budgetmonth'].dt.month == selected_month)
        ]
        if not monthly_budget.empty:
            monthly_budget = monthly_budget['totalbudget'].iloc[0]
        else:
            monthly_budget = 0  # or None, or some fallback value
            print(f"{labels['no_budget']}={userid()}, year={selected_year}, month={selected_month}")

        # filter categorical budgets for the logged-in user
        user_categorical_budgets = categorical_budgets[categorical_budgets['userid'] == userid()]

        net_balance = monthly_budget - total_spent
        print("Net Balance:", net_balance)  # Debugging statement

        net_balance_output = format_net_balance(net_balance)
        net_balance_output = html.Span(net_balance_output, className='netBalanceOutput')
        
        status_text, color = determine_status(monthly_budget, total_spent, selected_year, selected_month,labels)
        status_output = html.Span(status_text, style={'color': color}, className='statusOutput')

        expense_categorization_fig = update_expense_categorization_graph(filtered, labels, category_labels)
        daily_spending_trend_fig = update_daily_spending_trend_graph(filtered, monthly_budget, labels)
        budget_vs_actual_spending_fig = update_budget_vs_actual_spending_graph(filtered, user_categorical_budgets, labels, category_labels, lang)
        
        labels = get_dashboard_labels(lang)
        category_labels = get_category_labels(lang)
        transactions_tr = filtered.copy()
        transactions_tr['categoryname'] = transactions_tr['categoryname'].map(category_labels)
        transactions_tr['date_display'] = pd.to_datetime(transactions_tr['date']).dt.strftime('%Y-%m-%d')

        # for christ sake i've found the problem -_-
        transactions_table_data = transactions_tr.to_dict('records')

        # same order as in the output call-back
        return net_balance_output, status_output, expense_categorization_fig, daily_spending_trend_fig, budget_vs_actual_spending_fig, transactions_table_data

    def format_net_balance(net_balance):
        formatted_balance = net_balance
        formatted_balance = round(float(formatted_balance), 2)
        print("Formatted Balance:", formatted_balance)  # Debugging statement
        return formatted_balance

    def determine_status(monthly_budget, total_spent, selected_year, selected_month,labels):
        # key-value pairs
        status_label = {
            labels["status_label"]["excellent"]: "#00FF00",     
            labels["status_label"]["very_good"]: "#7FFF00",     
            labels["status_label"]["good"]: "#808080",          
            labels["status_label"]["fair"]: "#FFD700",          
            labels["status_label"]["needs_improv"]: "#FFA500",
            labels["status_label"]["poor"]: "#FF8C00",          
            labels["status_label"]["very_poor"]: "#FF4500",      
            labels["status_label"]["extremely_poor"]: "#FF0000",
            labels["status_label"]["critical"]: "#DC143C",      
            labels["status_label"]["severe"]: "#8B0000"         
        }

        daily_budget = calculated_daily_budget(monthly_budget, selected_year, selected_month)
        today = pd.Timestamp.today()
        if selected_year == today.year and selected_month == today.month:
            days_so_far = today.day
        else:
            days_so_far = pd.Period(f'{selected_year}-{selected_month}').days_in_month

        average_daily_spending = total_spent / days_so_far

        # used formula for calculating performance
        spent_percentage = (average_daily_spending/daily_budget) * 100

        if spent_percentage < 50:
            status_key = labels["status_label"]["excellent"]
        elif 50 <= spent_percentage < 70:
            status_key = labels["status_label"]["very_good"]
        elif 70 <= spent_percentage < 85:
            status_key = labels["status_label"]["good"]
        elif 85 <= spent_percentage < 95:
            status_key = labels["status_label"]["fair"]
        elif 95 <= spent_percentage < 100:
            status_key = labels["status_label"]["needs_improv"]
        elif 100 <= spent_percentage < 110:
            status_key = labels["status_label"]["poor"]
        elif 110 <= spent_percentage < 120:
            status_key = labels["status_label"]["very_poor"]
        elif 120 <= spent_percentage < 130:
            status_key = labels["status_label"]["extremely_poor"]
        elif 130 <= spent_percentage < 150:
            status_key = labels["status_label"]["critical"]
        else:
            status_key = labels["status_label"]["severe"]

        return status_key, status_label[status_key]

    def calculated_daily_budget(monthly_budget, year, month):
        days_in_month = pd.Period(f'{year}-{month}').days_in_month
        return monthly_budget/days_in_month

    def update_expense_categorization_graph(filtered, labels, category_labels):
        category_colors = {
            category_labels["Housing"]: "#FF5733",
            category_labels["Investments"]: "#1F77B4",
            category_labels["Debt Payments"]: "#2CA02C",
            category_labels["Healthcare"]: "#9467BD",
            category_labels["Food"]: "#FF69B4",
            category_labels["Entertainment & Leisure"]: "#17BECF",
            category_labels["Education"]: "#7F7F7F",
            category_labels["Transportation"]: "#C0C0C0",
            category_labels["Personal Care"]: "#FFA500",
            category_labels["Miscellaneous"]: "#FF4500"  
        }

        fig = px.pie(
            filtered, 
            values='amount', 
            names='categoryname', 
            color='categoryname',
            hole=0.3,
            color_discrete_map=category_colors,
            labels={
                'amount': labels['amount'],
                'categoryname': labels["category_type"]
            }
        )

        fig.update_traces(
            # textinfo='percent',  # show both percentage and label
            insidetextorientation='radial',
            textfont=dict(
                color='#000000',
                size=10
            )
        )

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                font=dict(
                    color="#000000",
                    size=10
                )
            )
        )

        return fig

    def update_daily_spending_trend_graph(filtered, monthly_budget, labels):
        # sum daily spending and calculate cumulative total
        daily_spending = filtered.groupby(filtered['date'].dt.day)['amount'].sum().cumsum().reset_index()
        daily_spending.columns = [labels['day_title'], labels['cumulative_spending_title']]

        # creating a new dataFrame, budget_line
        max_day = daily_spending[labels['day_title']].max()
        budget_line = pd.DataFrame({
            # creates a column named 'day' consisting of the values '1' and 'max_day'
            labels['day_title']: [1, max_day],
            'Total Budget': [monthly_budget, monthly_budget]
        })

        # adds a column called 'status' to the daily_spending dataFrame
        daily_spending[labels['status_title']] = daily_spending[labels['cumulative_spending_title']].apply(
            # x: The input value (each value in the Cumulative Spending column).
            lambda x: labels['under'] if x <= monthly_budget else labels['over']
        )

        # print("daily_spending: ")
        # print(daily_spending[:5])

        over_spending = pd.DataFrame() # Initialize an empty DataFrame
        over_index = daily_spending[daily_spending[labels['status_title']] == labels['over']].index.min()

        # iff there is an labels['over'] index, create two segments: labels['under'] and labels['over']
        if not pd.isna(over_index):
            under_spending = daily_spending.loc[:over_index]
            # .copy ensures that modifications to over_spending doesn't affect daily_spending
            over_spending = daily_spending.loc[over_index-1:].copy()
            # ensures that the first row of the over_spending DataFrame is correctly labeled as labels['over']
            over_spending.iloc[0, daily_spending.columns.get_loc(labels['status_title'])] = labels['over']
            # 1 for over_spending[1:] ensures that the first row is not duplicated  
            combined_spending = pd.concat([under_spending, over_spending[1:]])
        else:
            combined_spending = daily_spending

        fig = px.line(
            combined_spending,
            x=labels['day_title'],
            y=labels['cumulative_spending_title'],
            labels={
                labels['cumulative_spending_title']: labels['cumulative_spending'],
                labels['day_title']: labels["day"]
            },
            color=labels['status_title'],
            color_discrete_map={labels['under']: 'green', labels['over']: 'red'},
            markers=True
        )

        # add the labels['over'] segment if it exists
        if not over_spending.empty:
            fig.add_scatter(
                x=over_spending[labels['day_title']], 
                y=over_spending[labels['cumulative_spending_title']], 
                mode='lines+markers', 
                name=labels['over'], 
                line=dict(color='red', 
                width=3), 
                showlegend= False)
            
        # add budget line to the same figure
        fig.add_scatter(
            x=budget_line[labels['day_title']], 
            y=budget_line['Total Budget'], 
            mode='lines', 
            name=labels['monthly_budget'], 
            line=dict(
                color='#f8d44c', 
                dash='dash',
                width=5
            )
        )

        fig.update_traces(
            line=dict(width=3)
        ) 

        # customize the plot
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),  # left, right, top, bottom margins in pixels

            xaxis_tickangle=0,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, max_day + 1, 1)),  # tick every day
                tickfont=dict(
                    size=7,
                    color="#000000"
                ),
                title_font=dict(
                    color="#000000"),
                showgrid=False
            ),
            yaxis=dict(
                title_font=dict(color="#000000"),
                tickfont=dict(color="#000000"),
                showgrid=True,
                gridcolor='lightblue'
            ),
            legend=dict(
                title='',
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                font=dict(
                    color="#000000",
                    size=10
                )
            )
        )

        return fig

    def update_budget_vs_actual_spending_graph(filtered, categorical_budgets, labels, category_labels, lang):
        
        filtered = get_correct_category_labels(filtered, lang)

        actual_spending = filtered.groupby('categoryname')['amount'].sum().reset_index()
        budget_data = categorical_budgets[['categoryname', 'categorybudget']].groupby('categoryname').sum().reset_index() 

        summary = pd.merge(budget_data, actual_spending, on='categoryname', how='left')
        summary['categoryname'] = summary['categoryname'].map(category_labels)
        # print(filtered['categoryname'].unique())
        # print("--------------1\n",summary.head())
        summary.fillna(0, inplace=True)  # Replace NaN with 0 for categories with no spending

        summary.rename(columns={'categorybudget': labels['budget'], 'amount': labels['spent']}, inplace=True)
        
        # print("--------------2\n",summary.head())
        # print(summary.columns)
        # print(labels['budget'], labels['spent'])

        # create the bar chart for budget vs actual Spending
        fig = px.bar(
            summary, 
            x='categoryname', 
            y=[labels['budget'], labels['spent']],
            labels={
                'categoryname': labels['category_type'],
                'value': labels['amount'], # represented with 2 different y-values, so is labeled as 'value'
                'variable': '' # represented with 2 different y-values, so is labeled as 'value'
            },
            barmode='group',
            color_discrete_sequence=["#92154f", "#f19500"]
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_tickangle=45,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',

            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(
                    color="#000000",
                    size=10
                )
            ),
            xaxis=dict(
                title_font=dict(color="#000000"),  # color for the X-axis title
                tickfont=dict(
                    color="#000000",
                    size=10
                    ),  # color for the X-axis ticks
                showgrid=True,  # determines whether or not grid lines are drawn
                gridcolor='rgba(0,0,0,0)'  # color of grid lines
            ),
            yaxis=dict(
                title_font=dict(color="#000000"),  # color for the Y-axis title
                tickfont=dict(color="#000000"),  # color for the Y-axis ticks
                showgrid=True,  # determines whether or not grid lines are drawn
                gridcolor='lightblue'  # color of grid lines
            )
        )
                    
        return fig

