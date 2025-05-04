from datetime import datetime
from dash import Output, Input, State, no_update
import pandas as pd
from i18n.dashboard_labels import get_category_labels
from i18n.spendings_labels import get_spendings_callback_labels, get_spendings_labels
from utils.load_data import (get_max_id, load_categories, userid, load_local_categories, load_local_transactions, load_local_monthly_budgets, 
                            load_local_categorical_budgets, load_monthly_budgets, 
                            load_categorical_budgets, save_transactions, save_local_transactions, 
                            save_monthly_budgets, save_local_monthly_budgets, save_categorical_budgets, 
                            save_local_categorical_budgets, update_categorical_budget, update_monthly_budget, cache)
from utils.url_helpers import get_lang_from_query

def spendings_callback(app, use_remote_db=False):

    @app.callback(
        Output('transaction_status', 'children'),
        Input('submit_transaction', 'n_clicks'),
        [State('input_date', 'value'), 
        State('input_amount', 'value'), 
        State('input_category', 'value'), 
        State('input_description', 'value'),
        State('spendings-installment', 'value'),
        State('url','search')]
    )
    def add_transaction(n_clicks, date, amount, category, description, installment, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_spendings_labels(lang)

        current_time = datetime.now().strftime('%H:%M:%S')


        # TODO: check for remote db
        if n_clicks > 0 and date and amount and category and installment > 1:
            base_transaction = {
                'userid': userid(),
                'categoryname': category,
                'amount': amount / installment,
            }

            if use_remote_db:
                for i in range(installment):
                    current_transaction = base_transaction.copy()

                    installment_date = add_months_to_date(date, i)
                    current_transaction['date'] = f"{installment_date} {current_time}"
                    current_transaction['description'] = f"{description} ({i+1}/{installment})" if description else f"{category} ({i+1}/{installment})"

                    save_transactions(current_transaction)

            else:
                transactions = load_local_transactions()

                for i in range(installment):

                    if 'transactionid' in transactions.columns and not transactions['transactionid'].isnull().all():
                        next_id = transactions['transactionid'].max() + 1
                    else:
                        next_id = 0

                    current_transaction = base_transaction.copy()
                    current_transaction['transactionid'] = int(next_id)
                    transactions['transactionid'] = transactions['transactionid'].astype('Int64')

                    installment_date = add_months_to_date(date, i)
                    current_transaction['date'] = f"{installment_date} {current_time}"
                    current_transaction['description'] = f"{description} ({i+1}/{installment})" if description else f"{category} ({i+1}/{installment})"

                    transactions.loc[len(transactions)] = current_transaction

                save_local_transactions(transactions)

            return  f"Added {installment} installments of {amount / installment:.2f} for {category}" if lang == "en" else f"{labels['category']} için {installment} taksit eklendi, her bir taksit tutarı {amount / installment:.2f} olarak hesaplandı"

        elif n_clicks > 0 and date and amount and category:
            new_transaction = {
                'userid': userid(),
                'date': date,
                'categoryname': category,
                'amount': amount, 
                'description': description
            }

            if use_remote_db:
                save_transactions(new_transaction)
            else:
                transactions = load_local_transactions()

                # fix for nan transactionid values
                if 'transactionid' in transactions.columns and not transactions['transactionid'].isnull().all():
                    next_id = transactions['transactionid'].max() + 1
                else:
                    next_id = 0

                new_transaction['transactionid'] = int(next_id)
                transactions['transactionid'] = transactions['transactionid'].astype('Int64')

                new_transaction.update({'date': f'{date} {current_time}'})
                transactions.loc[len(transactions)] = new_transaction
                save_local_transactions(transactions)

            return f"{labels['transaction_added']} {date}, {amount}, {category}"


        elif n_clicks > 0:
            if not date:
                return labels['select_date']
            elif not amount:
                return labels['select_amount']
            elif not category:
                return labels["select_category"]
        return "" # button not clicked

    # update budget overview when new month is selected
    @app.callback(
        [Output('monthly_budget_status', 'children'),
        Output('budget_table', 'data'),
        Output('budget_overview_status', 'children')],
        [Input('slct_budget_month', 'value'),
        Input('slct_budget_year', 'value'),
        Input('update_trigger', 'children')],
        State("url","search")

    )
    # @cache.memoize()
    def display_budget(selected_month, selected_year, _, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_spendings_callback_labels(lang)
        category_labels = get_category_labels(lang)

        if use_remote_db:
            monthly_budgets = load_monthly_budgets()
            categorical_budgets = load_categorical_budgets()
        else:
            monthly_budgets = load_local_monthly_budgets()
            categorical_budgets = load_local_categorical_budgets()

            # filter for the logged in user
            monthly_budgets = monthly_budgets[monthly_budgets['userid'] == userid()]
            categorical_budgets = categorical_budgets[categorical_budgets['userid'] == userid()]

        print('Monthly Budgets\n', monthly_budgets[-5:])
        print('Categories Budgets\n', categorical_budgets[-5:])
        
        # monthly budget

        if selected_month and selected_year:
            # convert the selected month and year to a datetime object if valid selections
            selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01' + ' 00:00:00.000000')

            # filter the monthly budgets for the selected date
            monthly_budget_row = monthly_budgets[monthly_budgets['budgetmonth'] == selected_date]

            # display the total budget for the selected month, if not found show 0
            if monthly_budget_row.empty: #type: ignore
                total_budget = 0
            else:
                total_budget = int(monthly_budget_row['totalbudget'].values[0]) #type: ignore

            # Display the monhtly budget status message
            monthly_budget_status = f"{labels['your_budget']} {selected_date.strftime('%B %Y')} : {total_budget}₺"
        else:
            # display the last budget entry date if no month is selected
            last_entry_date = monthly_budgets['budgetmonth'].max()

            # if a budget entry is found, display the last entry month in the status message
            if last_entry_date is not pd.NaT:
                last_entry_month = last_entry_date.strftime('%B %Y')
                monthly_budget_status = f"{labels['last_budget_entry']} {last_entry_month}"
            else:
                monthly_budget_status = labels['no_budget_entry']

        # budget overview

        # display the allocated budget for each category in descending order
        budget_table_data = categorical_budgets.to_dict('records')
        
        # this converts to other languages
        for row in budget_table_data:
            original_name = row['categoryname']
            row['categoryname'] = category_labels.get(original_name, original_name)

        budget_table_data = sorted(budget_table_data, key=lambda x: x['categorybudget'], reverse=True)

        print("-----------------\n", budget_table_data)

        # if no data is found, load the categories and display the budget as 0 without saving
        if categorical_budgets.empty:
            if use_remote_db:
                categories = load_categories()
            else:
                categories = load_local_categories()

            for category in categories['name']:
                budget_table_data.append({'categoryname': category, 'categorybudget': 0})

        # hide the budget overview display message if no month is selected
        if not(selected_month and selected_year):
            budget_overview_status = ""
            return monthly_budget_status, budget_table_data, budget_overview_status
        
        # calculate the unallocated budget based on the total budget and category budgets
        unallocated_budget = int(total_budget - categorical_budgets['categorybudget'].sum())

        # customize the budget overview display message based on the budget surplus/deficit
        if unallocated_budget < 0:
            budget_overview_status = f"{labels['budget_exceeding']} ₺{-unallocated_budget}"
        elif unallocated_budget > 0:
            budget_overview_status = f"{labels['budget_remaining']} ₺{unallocated_budget}"
        else:
            budget_overview_status = f"${total_budget} Budget Fully Allocated"

        return monthly_budget_status, budget_table_data, budget_overview_status

    # update the total budget when a new total budget is submitted
    @app.callback(
        Output('total_budget_status', 'children'),
        [Input('submit_total_budget', 'n_clicks')],
        [State('slct_budget_month', 'value'), 
        State('slct_budget_year', 'value'), 
        State('input_total_budget', 'value'),
         State('url','search')]
    )

    def update_total_budget(n_clicks, selected_month, selected_year, total_budget, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_spendings_callback_labels(lang)

        if n_clicks > 0:
            if total_budget is None or total_budget == '':
                return labels['enter_total_budget'] 

            # convert the selected month and year to a datetime object
            selected_date = pd.to_datetime(f'{selected_year}-{selected_month:02d}-01')

            # load the latest budgets DB before updating
            if use_remote_db:
                monthly_budgets = load_monthly_budgets()
            else:
                monthly_budgets = load_local_monthly_budgets()

            # filter for the current user and selected date
            user_budget = monthly_budgets[(monthly_budgets['userid'] == userid()) 
                                                & (monthly_budgets['budgetmonth'] == selected_date)]

            if not user_budget.empty:
                if int(total_budget) == 0:
                    # remove the total budget for the selected month if set to 0
                    monthly_budgets = monthly_budgets[monthly_budgets.index != user_budget.index[0]]
                else:
                    # update the total budget for the selected month
                    if use_remote_db:
                        update_monthly_budget(userid(), selected_date, total_budget)
                        return labels['total_budget_updated'] 
                    else:
                        monthly_budgets.loc[user_budget.index, 'totalbudget'] = total_budget
            else:
                new_monthly_budget = {
                    'userid': userid(),
                    'totalbudget': total_budget,
                    'budgetmonth': selected_date
                }

                if not use_remote_db:
                    new_monthly_budget['budgetid'] = monthly_budgets['budgetid'].max() + 1
                    monthly_budgets.loc[len(monthly_budgets)] = new_monthly_budget

            # save the updated data to the database
            if use_remote_db:
                new_monthly_budget['budgetid'] = get_max_id(monthly_budgets) + 1
                save_monthly_budgets(new_monthly_budget)
            else:
                save_local_monthly_budgets(monthly_budgets)

            return labels['total_budget_updated'] 
        return ""

    # update the category budget when a new category budget is submitted
    @app.callback(
        Output('category_budget_status', 'children'),
        [Input('submit_category_budget', 'n_clicks')],
        [State('budget_category_dropdown', 'value'), 
        State('budget_category_input', 'value'),
        State("url","search")]
    )
    def update_category_budget(n_clicks, selected_category, new_category_budget, search):
        lang = get_lang_from_query(search) or "en"
        labels = get_spendings_callback_labels(lang)

        if n_clicks > 0:
            if selected_category and new_category_budget is not None:
                if use_remote_db:
                    categorical_budgets = load_categorical_budgets()
                else:
                    categorical_budgets = load_local_categorical_budgets()

                # filter for the user and selected category
                user_category = categorical_budgets[(categorical_budgets['userid'] == userid()) 
                                                          & (categorical_budgets['categoryname'] == selected_category)]

                # update the selected category's budget for the logged in user
                if not user_category.empty:
                    if use_remote_db:
                        update_categorical_budget(userid(), selected_category, new_category_budget)

                        return labels['category_budget_updated'] 
                    else:
                        categorical_budgets.loc[user_category.index, 'categorybudget'] = new_category_budget

                else:
                    new_category_budget_row = {
                        'userid': userid(),
                        'categoryname': selected_category,
                        'categorybudget': new_category_budget
                    }

                    if not use_remote_db:
                        new_category_budget_row['catbudgetid'] = categorical_budgets['catbudgetid'].max() + 1
                        categorical_budgets.loc[len(categorical_budgets)] = new_category_budget_row

                # save the updated data to the database
                if use_remote_db:
                    new_category_budget_row['catbudgetid'] = get_max_id('categoricalbudgets', 'catbudgetid') + 1
                    save_categorical_budgets(new_category_budget_row)
                else:
                    save_local_categorical_budgets(categorical_budgets)

                return labels['category_budget_updated'] 
            elif not selected_category:
                return labels['select_category']
            elif new_category_budget is None:
                return labels["enter_category_budget"]
        return ""

    # force an update to the budget table when a new category budget is submitted
    @app.callback(
        Output('update_trigger', 'children'),
        [Input('total_budget_status', 'children'),
         Input('category_budget_status', 'children')],
        State("url","search")
    )
    def trigger_update(total_budget_status, category_budget_status, search):

        lang = get_lang_from_query(search) or "en"
        labels = get_spendings_callback_labels(lang)

        if (total_budget_status == labels["total_budget_updated"]
            or category_budget_status == labels["category_budget_updated"]):
            return "Trigger Update"
        else:
            return no_update

    #@app.callback(
    #    Output('installment_value_display', 'children'),
    #    Input('input_installment', 'value')
    #)
    #def update_installment_display(value):
    #    if value == 0:
    #        return ""
    #    return f"Selected: {value} month{'s' if value > 1 else ''}"


def add_months_to_date(date_str, months):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    new_date = date_obj + relativedelta(months=months)
    return new_date.strftime('%Y-%m-%d')


def test_spendings(amount, category, installment, date, current_time, description, use_remote_db):
    pass
