def get_unauthorized_labels(lang="en"):
    all_labels = {
        "en": {
            "title": "Unauthorized",
            "message": "Please log in to view the dashboard.",
            "note": "If you believe this is an error, please contact support."
        },
        "tr": {
            "title": "Yetkisiz Erişim",
            "message": "Panoyu görüntülemek için lütfen giriş yapın.",
            "note": "Bunun bir hata olduğunu düşünüyorsanız, lütfen destek ile iletişime geçin."
        },
    }
    return all_labels.get(lang, all_labels["en"])
