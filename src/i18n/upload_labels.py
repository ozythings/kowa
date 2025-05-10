def get_upload_labels(lang="en"):
    all_labels = {
        "en": {
            "upload_title": "Upload Image",
            "upload_button": "Select a File",
            "select_type_title": "Select Type",
            "process_button": "Process",
            "add_transaction_button": "Add Transaction",
            "processed_data_title": "Processed Data",
            "amount_label": "Amount:",
            "date_label": "Date:",
            "category_label": "Category:",
            "description_label": "Description:",
            "raw_ocr_text_title": "Raw OCR Text",
            "drag_and_drop": "Drag and Drop or ",
            "time": "Time",
            "unknown_time": "Unknown Time",
            "receipt": "Receipt",
            "transaction_added": "Transaction added",
        },
        "tr": {
            "upload_title": "Görüntü Yükle",
            "upload_button": "Bir Dosya Seç",
            "select_type_title": "Tür Seç",
            "process_button": "İşlem Yap",
            "add_transaction_button": "İşlem Ekle",
            "processed_data_title": "İşlenmiş Veri",
            "amount_label": "Miktar:",
            "date_label": "Tarih:",
            "category_label": "Kategori:",
            "description_label": "Açıklama:",
            "raw_ocr_text_title": "İşlenmemiş OCR Metni",
            "drag_and_drop": "Sürükle bırak ya da ",
            "time": "Zaman",
            "unknown_time": "Bilinmeyen zaman",
            "receipt": "Fiş",
            "transaction_added": "İşlem eklendi",
        },
    }
    return all_labels.get(lang, all_labels["en"])

def get_upload_callback_labels(lang="en"):
    all_labels = {
        "en": {
            "upload_successful": "Upload successful!",
            "uploaded": "Uploaded",
            "select_date": "Please select a date",
            "enter_amount": "Please enter an amount",
            "select_category": "Please select a category",
            },
        "tr": {
            "upload_successful": "Yükleme başarılı!",
            "uploaded": "Yüklendi",
            "select_date": "Lütfen bir tarih seçin",
            "enter_amount": "Lütfen bir miktar girin",
            "select_category": "Lütfen bir kategori seçin",
        },
    }
    return all_labels.get(lang, all_labels["en"])
