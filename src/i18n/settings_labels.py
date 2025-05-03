def get_settings_labels(lang="en"):
    all_labels = {
        "en": {
            "title": "Settings",
            "description": "Adjust your preferences and manage your account settings here. Don't forget to save your changes.",
            "profile_section": {
                "title": "Profile",
                "name": "Name",
                "name_placeholder": "Your name",
                "email": "Email",
                "email_placeholder": "Your email",
                "update_button": "UPDATE PROFILE",
            },
            "change_password_section": {
                "title": "Change Password",
                "new_password": "New Password",
                "new_password_placeholder": "Your new password",
                "confirm_new_password": "Confirm New Password",
                "update_button": "UPDATE PASSWORD",
            },
            "delete_account_section": {
                "title": "Delete Account",
                "button": "Delete Account",
                "confirm_label": "Enter Password to Confirm",
                "confirm_button": "Confirm Delete"
            }
        },
        "tr": {
            "title": "Ayarlar",
            "description": "Tercihlerinizi ayarlayın ve hesap ayarlarınızı buradan yönetin. Değişiklikleri kaydetmeyi unutmayın.",
            "profile_section": {
                "title": "Profil",
                "name": "İsim",
                "name_placeholder": "Adınız",
                "email": "E-posta",
                "email_placeholder": "E-posta adresiniz",
                "update_button": "PROFİLİ GÜNCELLE",
            },
            "change_password_section": {
                "title": "Şifre Değiştir",
                "new_password": "Yeni Şifre",
                "new_password_placeholder": "Yeni şifreniz",
                "confirm_new_password": "Yeni Şifreyi Onayla",
                "update_button": "ŞİFREYİ GÜNCELLE",
            },
            "delete_account_section": {
                "title": "Hesabı Sil",
                "button": "Hesabı Sil",
                "confirm_label": "Onaylamak için şifrenizi girin",
                "confirm_button": "Silmeyi Onayla"
            }
        }
    }

    return all_labels.get(lang, all_labels["en"])
