def get_dashboard_labels(lang="en"):
    all_labels = {
        "en": {
            "year_month_title": "Year and Month",
            "select_year": "Select year:",
            "select_month": "Select month:",
            "net_balance_title": "Net Balance",
            "performance_title": "Performance",
            "expense_categorization_title": "Expense Categorization",
            "daily_spending_title": "Daily Spending Trend",
            "budget_vs_spending_title": "Budget vs. Spending Per Category",
            "recent_transactions_title": "Recent Transactions",
            "table_headers": {
                "date": "Date",
                "category": "Category Name",
                "amount": "Amount",
                "description": "Description"
            }
        },
        "tr": {
            "year_month_title": "Yıl ve Ay",
            "select_year": "Yılı seçin:",
            "select_month": "Ayı seçin:",
            "net_balance_title": "Net Bakiye",
            "performance_title": "Performans",
            "expense_categorization_title": "Gider Kategorileri",
            "daily_spending_title": "Günlük Harcama Eğilimi",
            "budget_vs_spending_title": "Kategoriye Göre Bütçe ve Harcama",
            "recent_transactions_title": "Son İşlemler",
            "table_headers": {
                "date": "Tarih",
                "category": "Kategori Adı",
                "amount": "Tutar",
                "description": "Açıklama"
            }
        }
    }

    return all_labels.get(lang, all_labels["en"])
