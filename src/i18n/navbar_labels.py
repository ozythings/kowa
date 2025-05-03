def get_navbar_labels(lang="en"):
    all_labels = {
        "en": {
            "dashboard": "Dashboard",
            "spendings": "Spendings",
            "upload": "Upload",
            "settings": "Settings",
            "logout": "Logout",
            "signin": "Sign in",
            "signup": "Sign up",
            "app_name": "kowa",
            "select_language": "Select Language"
        },
        "tr": {
            "dashboard": "Gösterge Paneli",
            "spendings": "Harcama",
            "upload": "Yükle",
            "settings": "Ayarlar",
            "logout": "Çıkış Yap",
            "signin": "Giriş Yap",
            "signup": "Kayıt Ol",
            "app_name": "kowa",
            "select_language": "Dil Seç"
        },
    }
    return all_labels.get(lang, all_labels["en"])
