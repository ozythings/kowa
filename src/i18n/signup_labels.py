def get_signup_labels(lang="en"):
    all_labels = {
        "en": {
            "title": "Sign Up",
            "name_placeholder": "Your name",
            "email_placeholder": "Your email",
            "password_placeholder": "Password",
            "confirm_password_placeholder": "Re-enter your password",
            "register_button": "Register",
            "already_have_account": "Already have an account? ",
            "signin_link": "Sign in",
            "illustration_alt": "illustration",
            "signup_status": "Please ensure all fields are filled correctly.",
        },
        "tr": {
            "title": "Kayıt Ol",
            "name_placeholder": "Adınız",
            "email_placeholder": "E-posta adresiniz",
            "password_placeholder": "Şifre",
            "confirm_password_placeholder": "Şifrenizi yeniden girin",
            "register_button": "Kaydol",
            "already_have_account": "Zaten hesabınız var mı? ",
            "signin_link": "Giriş Yap",
            "illustration_alt": "illüstrasyon",
            "signup_status": "Lütfen tüm alanları doğru şekilde doldurduğunuzdan emin olun.",
        },
    }
    return all_labels.get(lang, all_labels["en"])
