def get_signin_labels(lang="en"):
    all_labels = {
        "en": {
            "title": "Sign In",
            "username_placeholder": "Username",
            "password_placeholder": "Password",
            "login_button": "Login",
            "login_message": "Please enter your credentials to sign in.",
            "illustration_alt": "illustration",
        },
        "tr": {
            "title": "Giriş Yap",
            "username_placeholder": "Kullanıcı Adı",
            "password_placeholder": "Şifre",
            "login_button": "Giriş Yap",
            "login_message": "Giriş yapmak için bilgilerinizi girin.",
            "illustration_alt": "illüstrasyon",
        },
    }
    return all_labels.get(lang, all_labels["en"])

