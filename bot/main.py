import json
import logging

import aiohttp

from database.mongo import settings
from utils.exceptions.telegram import TelegramSendMessageError, TelegramSendPhotoError, TelegramSendMediaGroupError
from utils.models import CustomMediaChunks
from utils.models import Post
from utils.text_sevice import chunks_to_text, correct_caption_len


logger = logging.getLogger(__name__)


async def send_news(post: Post, channel_tg_id, mongo):
    # TODO: Bad Request: failed to send message #1 with the error message "WEBPAGE_MEDIA_EMPTY"
    media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=True)
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
            try:
                await send_media_group(channel_id=chat_id, media=media, post=post)
            except TelegramSendMediaGroupError as error:
                logger.error(f'{error.message}')

        else:
            caption = correct_caption_len(caption)
            caption += f'<a href="{image_link}">&#160</a>'
            try:
                await send_message(text=caption, channel_id=chat_id, post=post)
            except TelegramSendMessageError as error:
                logger.error(f'{error.message}')
    else:
        if len(caption) >= 1024:
            caption = correct_caption_len(caption)
        try:
            await send_message(channel_id=channel_tg_id, text=caption, post=post)
        except TelegramSendMessageError as error:
            logger.error(f'{error.message}')

    mongo.update_news_set_posted(news_id=post.oid)
    mongo.update_news_body_ai(news_id=post.oid, body=post.body)


async def send_message(text: str, channel_id: int, post: Post):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'
    data = {
            'chat_id': channel_id,
            'text': text,
            'parse_mode': 'HTML'
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response = await response.json()
        if not response['ok']:
            raise TelegramSendMessageError(post=post, response=response, tg_text=text)


async def send_photo(caption: str, photo: str, channel_id: int, post: Post):
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
            raise TelegramSendPhotoError(post=post, response=response, photo=photo, caption=caption)


async def send_media_group(media: list[dict], channel_id: int, post: Post):
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMediaGroup'
    data = {
            'chat_id': channel_id,
            'media': json.dumps(media)
            }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response = await response.json()
        if not response['ok']:
            raise TelegramSendMediaGroupError(post=post, response=response, media=media)


if __name__ == '__main__':
    ...
