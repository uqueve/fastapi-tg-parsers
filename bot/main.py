import asyncio
import json
import pprint

import aiohttp

from database.mongo import settings
from utils.models import CustomMediaChunks
from utils.models import Post
from utils.text_sevice import chunks_to_text, correct_caption_len


async def send_news(post: Post, channel_tg_id, mongo):
    # TODO: set convert_with_ai=True
    media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=False)
    media = media_chunks.get_media()
    chunks = media_chunks.get_text_chunks()
    image_link = media_chunks.get_link()

    caption = chunks_to_text(chunks)

    chat_id = channel_tg_id

    if media is not None:

        if len(caption) < 1024:
            print(1)
            media[0]['caption'] = caption
            media[0]['parse_mode'] = 'HTML'
            await send_media_group(channel_id=chat_id, media=media)

        else:
            caption = correct_caption_len(caption)
            caption += f'<a href="{image_link}">&#160</a>'

            await send_message(text=caption, channel_id=chat_id)
    else:
        if len(caption) >= 1024:
            caption = correct_caption_len(caption)
        await send_message(channel_id=channel_tg_id, text=caption)

    mongo.update_news_set_posted(news_id=post.oid)
    mongo.update_news_body_ai(news_id=post.oid, body=post.body)


async def send_message(text: str, channel_id: int):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'
    data = {
            'chat_id': channel_id,
            'text': text,
            'parse_mode': 'HTML'
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response = await response.json()
        if not response['ok']:
            print(f'Ошибка при отправке новости: {response}')


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
            print(f'Ошибка при отправке новости: {response}')


async def send_media_group(media: list[dict], channel_id: int):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMediaGroup'
    data = {
            'chat_id': channel_id,
            'media': json.dumps(media)
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response = await response.json()
        if not response['ok']:
            print(f'Ошибка при отправке новости: {response}')


if __name__ == '__main__':
    # post = Post(title='В Гане мать заживо закопала младенца, но он чудом выжил после шести часов под землей',
    #             body='В Гане мать заживо закопала новорожденного ребенка в саду, младенца удалось спасти, он провел под землей несколько часов.\nКак передает Report, об этом сообщает Daily Mail.\nСогласно информации, 23-летняя женщина родила девочку дома и, решив избавиться от младенца, закопала его в саду. Новорожденную обнаружили родственники, она провела под землей шесть часов. Тело девочки было в синяках и царапинах, но ее удалось спасти и доставить в больницу. Спустя неделю ее выписали из медучреждения и передали родственникам.\nМать девочки задержали, она помещена в психиатрическую лечебницу. Обстоятельства, побудившие женщину закопать ребенка заживо, устанавливаются.\n',
    #             image_links=['https://static.report.az/photo/c62f4eba-a253-376d-8d40-84cd753abb61_850.jpg',],
    #             link='https://report.az/ru/drugie-strany/v-gane-mat-zazhivo-zakopala-mladenca-no-on-chudom-vyzhil-posle-shesti-chasov-pod-zemlej/')
    # media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=False)
    # mediaa = media_chunks.get_media()
    # chunks = media_chunks.get_text_chunks()
    # image_link = media_chunks.get_link()
    # caption = chunks_to_text(chunks)
    # mediaa[0]['caption'] = post.get_text()
    # asyncio.run(send_media_group(media=mediaa, channel_id=-1002014480454))
    # asyncio.run(send_news(mongo=None, post=post, channel_tg_id=-1002014480454))
    # asyncio.run(send_message(text=caption, channel_id=-1002014480454))
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
