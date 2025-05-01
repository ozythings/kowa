
def get_temp_labels(lang="en"):
    labels = {

    }[lang]

    return labels.get(lang, labels["en"])

def get_spendings_labels(lang="en"):
    all_labels = {
        "en": {
            "title": "Spendings",
            "submit": "Submit",
            "add_transaction": "Add Transaction",
            "select_date": "Select date",
            "amount": "Amount",
            "category": "Category",
            "description": "Description",
            "monthly_budget": "Monthly Budget",
            "month": "Month",
            "year": "Year",
            "budget": "Budget",
            "update": "Update",
            "category_budget": "Category Budget",
            "set": "Set",
            "budget_overview": "Budget Overview"
        },
        "tr": {
            "title": "Harcamalar",
            "submit": "Gönder",
            "add_transaction": "İşlem Ekle",
            "select_date": "Tarih Seç",
            "amount": "Miktar",
            "category": "Kategori",
            "description": "Açıklama",
            "monthly_budget": "Aylık Bütçe",
            "month": "Ay",
            "year": "Yıl",
            "budget": "Bütçe",
            "update": "Güncelle",
            "category_budget": "Kategori Bütçesi",
            "set": "Ayarla",
            "budget_overview": "Bütçe Özeti"
        }
    }

    return all_labels.get(lang, all_labels["en"])
