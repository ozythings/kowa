from dash import html, Input, Output
import pandas as pd
import plotly.express as px
from utils.load_data import userid, load_database, cache

def dashboard_callback(app, use_remote_db=False):

    @app.callback(
        [Output('net-balance-output', 'children'), 
        Output('status-output', 'children'),
        Output('expense_categorization_graph', 'figure'), 
        Output('daily_spending_trend_graph', 'figure'),
        Output('budget_vs_actual_spending_graph', 'figure'),
        Output('transactions_table', 'data')],

        [Input('slct_year', 'value'),
        Input('slct_month', 'value')]
    )
    @cache.memoize()
    def update_graph(selected_year, selected_month):
        # load data from the database
        transactions, monthly_budgets, categorical_budgets = load_database(use_remote_db)

        # filters to only include rows where the year and month match the input year and month for the logged-in user
        # boolean indexing: [ ] filters rows based on a condition
        filtered = transactions[(transactions['userid'] == userid()) &
                                    (transactions['date'].dt.year == selected_year) &
                                    (transactions['date'].dt.month == selected_month)]

        # ensure the dataframe is not empty
        if filtered.empty:
            return 'No transactions found', '', {}, {}, {}, []

        # total spent in a month
        total_spent = filtered['amount'].sum()

        # converting to date-time
        monthly_budgets['budgetmonth'] = pd.to_datetime(monthly_budgets['budgetmonth'])

        # .iloc[0] retrieves the first value from the resulting series
        monthly_budget = monthly_budgets[
            (monthly_budgets['userid'] == userid()) &
            (monthly_budgets['budgetmonth'].dt.year == selected_year) &
            (monthly_budgets['budgetmonth'].dt.month == selected_month)
        ]['totalbudget'].iloc[0]
        # TODO: Handle the case where there is monthly budget available for the selected month (currently throws callback errors)

        # filter categorical budgets for the logged-in user
        user_categorical_budgets = categorical_budgets[categorical_budgets['userid'] == userid()]

        net_balance = monthly_budget - total_spent
        print("Net Balance:", net_balance)  # Debugging statement

        net_balance_output = net_balance #format_net_balance(net_balance)
        net_balance_output = html.Span(net_balance_output, className='netBalanceOutput')
        
        status_text, color = determine_status(monthly_budget, total_spent, selected_year, selected_month)
        status_output = html.Span(status_text, style={'color': color}, className='statusOutput')

        expense_categorization_fig = update_expense_categorization_graph(filtered)
        daily_spending_trend_fig = update_daily_spending_trend_graph(filtered, monthly_budget)
        budget_vs_actual_spending_fig = update_budget_vs_actual_spending_graph(filtered, user_categorical_budgets)
        
        transactions_table_data = filtered[['date', 'categoryname', 'amount', 'description']].to_dict('records')

        # same order as in the output call-back
        return net_balance_output, status_output, expense_categorization_fig, daily_spending_trend_fig, budget_vs_actual_spending_fig, transactions_table_data

    def format_net_balance(net_balance):
        if net_balance < 0:
            formatted_balance = f"({-net_balance})"
        else:
            formatted_balance = str(net_balance)
        print("Formatted Balance:", formatted_balance)  # Debugging statement
        return formatted_balance

    def determine_status(monthly_budget, total_spent, selected_year, selected_month):
        # key-value pairs
        status_colors = {
            "EXCELLENT": "#00FF00",     
            "VERY GOOD": "#7FFF00",     
            "GOOD": "#FFFF00",          
            "FAIR": "#FFD700",          
            "NEEDS IMPROVEMENT": "#FFA500",
            "POOR": "#FF8C00",          
            "VERY POOR": "#FF4500",      
            "EXTREMELY POOR": "#FF0000",
            "CRITICAL": "#DC143C",      
            "SEVERE": "#8B0000"         
        }

        daily_budget = calculated_daily_budget(monthly_budget, selected_year, selected_month)
        today = pd.Timestamp.today()
        if selected_year == today.year and selected_month == today.month:
            days_so_far = today.day
        else:
            days_so_far = pd.Period(f'{selected_year}-{selected_month}').days_in_month

        average_daily_spending = total_spent / days_so_far
        spent_percentage = (average_daily_spending/daily_budget) * 100

        if spent_percentage < 50:
            status_key = "EXCELLENT"
        elif 50 <= spent_percentage < 70:
            status_key = "VERY GOOD"
        elif 70 <= spent_percentage < 85:
            status_key = "GOOD"
        elif 85 <= spent_percentage < 95:
            status_key = "FAIR"
        elif 95 <= spent_percentage < 100:
            status_key = "NEEDS IMPROVEMENT"
        elif 100 <= spent_percentage < 110:
            status_key = "POOR"
        elif 110 <= spent_percentage < 120:
            status_key = "VERY POOR"
        elif 120 <= spent_percentage < 130:
            status_key = "EXTREMELY POOR"
        elif 130 <= spent_percentage < 150:
            status_key = "CRITICAL"
        else:
            status_key = "SEVERE"

        return status_key, status_colors[status_key]

    def calculated_daily_budget(monthly_budget, year, month):
        days_in_month = pd.Period(f'{year}-{month}').days_in_month
        return monthly_budget/days_in_month

    def update_expense_categorization_graph(filtered):
        category_colors = {
            "Housing": "#FF5733",
            "Investments": "#1F77B4",
            "Debt Payments": "#2CA02C",
            "Healthcare": "#9467BD",
            "Food": "#FF69B4",
            "Entertainment & Leisure": "#17BECF",
            "Education": "#7F7F7F",
            "Transportation": "#C0C0C0",
            "Personal Care": "#FFA500",
            "Miscellaneous": "#FF4500"  
        }

        fig = px.pie(
            filtered, 
            values='amount', 
            names='categoryname', 
            color='categoryname',
            hole=0.3,
            color_discrete_map=category_colors
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

    def update_daily_spending_trend_graph(filtered, monthly_budget):
        # sum daily spending and calculate cumulative total
        daily_spending = filtered.groupby(filtered['date'].dt.day)['amount'].sum().cumsum().reset_index()
        daily_spending.columns = ['Day', 'Cumulative Spending']

        # creating a new dataFrame, budget_line
        max_day = daily_spending['Day'].max()
        budget_line = pd.DataFrame({
            # creates a column named 'day' consisting of the values '1' and 'max_day'
            'Day': [1, max_day],
            'Total Budget': [monthly_budget, monthly_budget]
        })

        # adds a column called 'status' to the daily_spending dataFrame
        daily_spending['Status'] = daily_spending['Cumulative Spending'].apply(
            # x: The input value (each value in the Cumulative Spending column).
            lambda x: 'Under' if x <= monthly_budget else 'Over'
        )

        print("daily_spending: ")
        print(daily_spending[:5])

        over_spending = pd.DataFrame() # Initialize an empty DataFrame
        over_index = daily_spending[daily_spending['Status'] == 'Over'].index.min()

        # iff there is an 'Over' index, create two segments: 'Under' and 'Over'
        if not pd.isna(over_index):
            under_spending = daily_spending.loc[:over_index]
            # .copy ensures that modifications to over_spending doesn't affect daily_spending
            over_spending = daily_spending.loc[over_index-1:].copy()
            # ensures that the first row of the over_spending DataFrame is correctly labeled as 'Over'
            over_spending.iloc[0, daily_spending.columns.get_loc('Status')] = 'Over'
            # 1 for over_spending[1:] ensures that the first row is not duplicated  
            combined_spending = pd.concat([under_spending, over_spending[1:]])
        else:
            combined_spending = daily_spending

        fig = px.line(
            combined_spending,
            x='Day',
            y='Cumulative Spending',
            labels={
                'Cumulative Spending': 'cumulative spending ($)',
                'Day': 'day'
            },
            color='Status',
            color_discrete_map={'Under': 'green', 'Over': 'red'},
            markers=True
        )

        # add the 'Over' segment if it exists
        if not over_spending.empty:
            fig.add_scatter(
                x=over_spending['Day'], 
                y=over_spending['Cumulative Spending'], 
                mode='lines+markers', 
                name='Over', 
                line=dict(color='red', 
                width=3), 
                showlegend= False)
            
        # add budget line to the same figure
        fig.add_scatter(
            x=budget_line['Day'], 
            y=budget_line['Total Budget'], 
            mode='lines', 
            name='Monthly Budget', 
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

    def update_budget_vs_actual_spending_graph(filtered, categorical_budgets):
        # merge actual spending data with budgets data
        actual_spending = filtered.groupby('categoryname')['amount'].sum().reset_index()
        budget_data = categorical_budgets[['categoryname', 'categorybudget']].groupby('categoryname').sum().reset_index() 
        
        # merging the actual spending with the budgets
        summary = pd.merge(budget_data, actual_spending, on='categoryname', how='left')
        summary.fillna(0, inplace=True)  # Replace NaN with 0 for categories with no spending

        summary.rename(columns={'categorybudget': 'Budget', 'amount': 'Spent'}, inplace=True)

        # create the bar chart for budget vs actual Spending
        fig = px.bar(
            summary, 
            x='categoryname', 
            y=['Budget', 'Spent'],
            labels={
                'categoryname': 'category types',
                'value': 'amount ($)', # represented with 2 different y-values, so is labeled as 'value'
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
