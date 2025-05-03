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

def get_dashboard_callback_labels(lang="en"):
    all_labels = {
        "en": {
            "status_label": {
                "excellent": "EXCELLENT", 
                "very_good": "VERY GOOD",
                "good": "GOOD",
                "fair":"FAIR",
                "needs_improv": "NEEDS IMPROV",
                "poor":"POOR",
                "very_poor":"VERY POOR",
                "extremely_poor":"EXTREMELY POOR",
                "critical":"CRITICAL",
                "severe": "SEVERE",
            },
            "total_spent": "Total spent: ${:,.2f}",
            "net_balance": "Net Balance: ${:,.2f}",
            "status": "Status: {status}",
            "under_budget": "Under budget",
            "over_budget": "Over budget",
            "monthly_budget": "Monthly Budget",
            "no_transaction": "No transactions found",
            "no_budget": "No budget found for user",
            "year": "year",
            "month": "month",
            "day_title": "Day",
            "day": "day",
            "cumulative_spending_title": "Cumulative Spending",
            "cumulative_spending": "cumulative spending (₺)",
            "over": "Over",
            "under": "Under",
            "total_budget": "Total Budget",
            "status_title": "Status",
            "budget": "budget",
            "budget_title": "Budget",
            "spent": "spent",
            "spent_title": "Spent",
            "amount": "amount",
            "category_type": "category"
        },
        "tr": {

            "status_label": {
                "excellent": "MÜKEMMEL", 
                "very_good": "ÇOK İYİ",
                "good": "İYİ",
				"fair": "ORTA",
                "needs_improv": "İYİLEŞME GEREK",
                "poor":"KÖTÜ",
                "very_poor":"ÇOK KÖTÜ",
                "extremely_poor":"AŞIRI KÖTÜ",
                "critical":"KRİTİK",
                "severe": "İFLASVARİ",
            },
            "total_spent": "Toplam harcama: ${:,.2f}",
            "net_balance": "Net bakiye: ${:,.2f}",
            "status": "Durum: {status}",
            "under_budget": "Bütçe altında",
            "over_budget": "Bütçe üzerinde",
            "monthly_budget": "Aylık Bütçe",
            "no_transaction": "İşlem bulunmadı",
            "no_budget": "Kullanıcı için bütçe bulunamadı",
            "year": "yıl",
            "month": "ay",
            "day_title": "Gün",
            "day": "gün",
            "cumulative_spending_title": "Kümülatif Harcama",
            "cumulative_spending": "kümülatif harcama (₺)",
            "over": "Üstünde",
            "under": "Altında",
            "total_budget": "Toplam Bütçe",
            "status_title": "Durum",
            "budget": "Bütçe",
            "spent": "Harcama",
            "amount": "miktar",
            "category_type": "kategori"
        }
    }

    return all_labels.get(lang, all_labels["en"])

def get_category_labels(lang="en"):
    category_labels = {
        "en": {
            "Housing": "Housing",
            "Transportation": "Transportation",
            "Food": "Food",
            "Healthcare": "Healthcare",
            "Debt Payments": "Debt Payments",
            "Investments": "Investments",
            "Entertainment & Leisure": "Entertainment & Leisure",
            "Personal Care": "Personal Care",
            "Education": "Education",
            "Miscellaneous": "Miscellaneous",
        },
        "tr": {
            "Housing": "Barınma",
            "Transportation": "Ulaşım",
            "Food": "Yemek",
            "Healthcare": "Sağlık",
            "Debt Payments": "Borç ödemesi",
            "Investments": "Yatırım",
            "Entertainment & Leisure": "Eğlence",
            "Personal Care": "Kişisel Bakım",
            "Education": "Eğitim",
            "Miscellaneous": "Çeşitli",
        }
    }
    return category_labels.get(lang, category_labels["en"])

def get_correct_category_labels(filtered, lang="en"):
    if lang == "tr":
        labels = get_category_labels("tr")
        category_mapping = {v: k for k, v in labels.items()}
        
        filtered['categoryname'] = filtered['categoryname'].map(category_mapping)
    
    return filtered
