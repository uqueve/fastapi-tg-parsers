import logging

import openai

from config_data.config import get_settings


class OpenAIService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.OPENAI_KEY
        self.url = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        self.proxies = {
            'http': 'http://4CLjka:LKAMRJ@45.130.126.30:8000',
        }

    def make_request(self, texts: str, max_tokens=8000):
        prompt = (
            f'Перепиши текст более художественно на русском языке, сохраняя смысл, и сократи его до размера '
            f'очень короткого поста.'
            f'Пост не может быть длиннее 400 символов, строго! Убери лишние упоминания и ссылки в тексте, сделай '
            f'текст красивым и презентабельным, расставь абзацы, удали все упоминания источника и все элементы '
            f'в квадратных скобках. Текст для обработки: {texts}'
        )

        try:
            openai.api_key = self.api_key

            response = openai.chat.completions.create(
                model='gpt-4-1106-preview',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.exception(f'\t\t- An unexpected error occurred: {e}')
            return texts

    def translate_title_request(self, title: str, max_tokens=8000):
        prompt = f'Переведи этот текст на русский: {title}'

        try:
            openai.api_key = self.api_key

            response = openai.chat.completions.create(
                model='gpt-4-1106-preview',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.exception(f'\t\t- An unexpected error occurred: {e}')
            return title


if __name__ == '__main__':
    oi = OpenAIService()
    print(
        oi.make_request(
            texts="""
        Один из самых больших домов в Америке, замок Херст стал источником восхищения американцев с тех пор, 
        как Уильям Рэндольф Херст начал строить его в 1919 году. Расположенное к северу от Сан-Луис-Обиспо, 
        недалеко от шоссе №1, впечатляющее поместье, спроектированное архитектором Джулией Морган, 
        примечательно не только своими размерами, но и невероятной коллекцией произведений искусства и 
        антиквариата, приобретенных Херстом со всего мира. На протяжении всего пребывания Херста в замке 
        Сан-Симеон дом привлекал внимание многих представителей Голливуда и политики, от Греты Гарбо и Чарли 
        Чаплина до Уинстона Черчилля и Кэлвина Кулиджа. Считается, что Херст и его особняк вдохновили Чарльза 
        Фостера Кейна из "Гражданина Кейна" и его готический "Ксанаду", что еще больше усилило интерес к знаменитому 
        недостроенному замку. Читайте дальше, чтобы узнать историю и чудеса одного из самых культовых домов Америки.
        Здание построено в 1958 году
        Сенатор, старатель и бизнесмен Джордж Херст
    """,
        ),
    )
