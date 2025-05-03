
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
            "budget_overview": "Budget Overview",
            "top_info": 'Enter your expenses and customize your budget categories on this page to keep your finances organized and under control.',
            "financial_management": "Financial Management",
            "installment": "Installment (months)",
            "no_installment": "No Installment",
            "enter_amount": "enter amount",
            "select_category": "select category",
            "enter_description": "enter description",
            "select_month": "select month",
            "select_year": "select year",
            "enter_budget": "enter budget",
            "add": "ADD",
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
            "budget_overview": "Bütçe Özeti",
            "top_info": "Bu sayfada harcamalarınızı girin ve bütçe kategorilerinizi özelleştirerek finansmanınızı düzenli tutun ve kontrol altında tutun.",
            "financial_management": "Finans Yönetimi",
            "installment": "Taksit (Ay)",
            "no_installment": "Taksit Yok",
            "enter_amount": "miktar gir",
            "select_category": "kategori gir",
            "enter_description": "açıklama gir",
            "select_month": "ay seç",
            "select_year": "yıl seç",
            "enter_budget": "bütçe gir",
            "add": "EKLE",
        }
    }

    return all_labels.get(lang, all_labels["en"])

def get_spendings_callback_labels(lang="en"):
    all_labels = {
        "en": {
            "transaction_added": "Transaction added",
            "select_date": "Please select a date",
            "enter_amount": "Please enter an amount",
            "select_category": "Please select a category",
            "your_budget": "Your current budget for",
            "last_budget_entry": "Your last budget entry was in",
            "no_budget_entry": "No past budget entries found",
            "budget_exceeding": "Exceeding current monthly budget by ${unallocated_budget}",
            "budget_remaining": "Remaining monthly budget of ${unallocated_budget}",
            "budget_fully_allocated": "${total_budget} Budget Fully Allocated",
            "enter_total_budget": "Please enter a total budget",
            "total_budget_updated": "Total budget updated successfully!",
            "category_budget_updated": "Category budget updated successfully!",
            "enter_category_budget": "Please enter a budget amount",
            "trigger_update": "Trigger Update"
        },
        "tr": {
            "transaction_added": "Harcama eklendi",
            "select_date": "Lütfen bir tarih seçin",
            "enter_amount": "Lütfen bir miktar girin",
            "select_category": "Lütfen bir kategori seçin",
            "your_budget": "Şu anki bütçeniz",
            "last_budget_entry": "Son bütçe girişiniz",
            "no_budget_entry": "Önceki bütçe girişi bulunamadı",
            "budget_exceeding": "Aylık bütçenizi ${unallocated_budget} aşan harcama",
            "budget_remaining": "Kalan aylık bütçe ${unallocated_budget}",
            "budget_fully_allocated": "${total_budget} Bütçe Tamamen Dağıtıldı",
            "enter_total_budget": "Lütfen toplam bir bütçe girin",
            "total_budget_updated": "Toplam bütçe başarıyla güncellendi!",
            "category_budget_updated": "Kategori bütçesi başarıyla güncellendi!",
            "select_category_error": "Lütfen bir kategori seçin",
            "enter_category_budget": "Lütfen bir bütçe miktarı girin",
            "trigger_update": "Güncelleme Tetiklendi"
        }
    }

    return all_labels.get(lang, all_labels["en"])

