import logging

import requests

from utils.models import Post


def translate_text(texts: str, target_language: str = 'ru') -> str:
    try:
        data = b'{"yandexPassportOauthToken":"y0_AgAAAAByTWu7AATuwQAAAADyypgU_2k4iKydQReazwI8W5piOM_1sLg"}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(
            'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            headers=headers,
            data=data,
        )
        IAM_TOKEN = response.json()['iamToken']
        folder_id = 'b1ghr5r12cott99s7tbt'

        body = {
            'targetLanguageCode': target_language,
            'texts': texts,
            'folderId': folder_id,
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {IAM_TOKEN}',
        }

        response = requests.post(
            'https://translate.api.cloud.yandex.net/translate/v2/translate',
            json=body,
            headers=headers,
        )

        return response.json()['translations'][0]['text']

    except Exception:
        logging.exception('Error in text translating')
        return texts + '\n\nОшибка перевода текста. Проверьте токен или баланс!'


def translate_post(post: Post) -> Post:
    new_post: Post = Post(
        title=translate_text(post.title),
        body=translate_text(post.body),
        image_links=post.image_links,
    )

    return new_post


def translate_posts(posts: list) -> list:
    return list(map(translate_post, posts))
    # return [translate_post(post) for post in posts]
