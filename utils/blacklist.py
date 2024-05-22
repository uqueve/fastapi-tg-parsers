blacklist_words: list = [
    'Билайн',
    'lenta.com',
    'Вместе24',
    'МТС',
    '1XBET',
    'APK',
    'пари',
    'с подпиской',
    'email protected',
]


def blackword_in_news_validate(body: str) -> dict:
    for word in blacklist_words:
        if word in body:
            return {'ok': False, 'word': word}
    return {'ok': True, 'word': None}
