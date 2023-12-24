LANGUAGES = {
    'ru': 'Русский',
    'en': 'Английский',
    'fr': 'Французкий',
    'zh-cn': 'Китайский',
    'ko': 'Корейский',
    'uz': 'Узбекский'
}

def get_key(lang):
    for key, value in LANGUAGES.items():
        if lang == value:
            return key