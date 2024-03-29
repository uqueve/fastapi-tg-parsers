import asyncio
import json
import pprint

import aiohttp

from database.mongo import settings
from utils.models import CustomMediaChunks
from utils.models import Post
from utils.text_sevice import chunks_to_text, correct_caption_len


async def send_news(post: Post, channel_tg_id, mongo):
    media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=False)
    media = media_chunks.get_media()
    chunks = media_chunks.get_text_chunks()
    image_link = media_chunks.get_link()

    caption = chunks_to_text(chunks)

    chat_id = channel_tg_id

    if media is not None:

        if len(caption) < 1024:
            media[0]['caption'] = caption
            await send_media_group(chat_id, media)

        else:
            caption = correct_caption_len(caption)
            caption += f'<a href="{image_link}">&#160</a>'

            await send_message(caption, chat_id)
    else:
        if len(caption) >= 1024:
            caption = correct_caption_len(caption)
        await send_message(channel_id=channel_tg_id, text=caption)

    mongo.update_news_set_posted(news_id=post.id)
    mongo.update_news_body_ai(news_id=post.id, body=post.body)


async def send_message(text: str, channel_id: int):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'
    data = {
            'chat_id': channel_id,
            'text': text,
            'parse_mode': 'HTML'
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        print(await response.json())


async def send_photo(caption: str, photo: str, channel_id: int):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendPhoto'
    data = {
            'chat_id': channel_id,
            'photo': photo,
            'caption': caption,
            'parse_mode': 'HTML'
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response = await response.json()
        if not response['ok']:
            ...
        print(response)


async def send_media_group(media: list[dict], channel_id: int):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMediaGroup'
    data = {
            'chat_id': channel_id,
            'media': json.dumps(media)
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        print(await response.json())


if __name__ == '__main__':
    # post = Post(title='Какой-то заголовок',
    #             body='Какой-то текст для прикладывания к фотографии и отправке в телеграм канал',
    #             image_links=['https://i.imgur.com/VZPMImv.jpg', 'https://i.imgur.com/VZPMImv.jpg'],
    #             link='https://i.imgur.com/VZPMImv.jpg')
    # media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=False)
    # media = media_chunks.get_media()
    # chunks = media_chunks.get_text_chunks()
    # image_link = media_chunks.get_link()
    #
    # caption = chunks_to_text(chunks)
    # media.caption = caption
    # pprint.pprint(post.get_text())
    # pprint.pprint(caption)
    # print(media)
    # caption = 'Какой-то текст сообщения для поста в телеграм'
    # image_link = 'https://i.imgur.com/VZPMImv.jpg'
    # caption = correct_caption_len(caption)
    # caption += f'<a href="{image_link}">&#160</a>'
    # asyncio.run(send_message(
    #     text=caption,
    #     channel_id=-1002014480454
    # ))
    ...
