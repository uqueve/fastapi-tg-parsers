import json
import logging

import aiohttp

from database.mongo import NewsRepository, settings
from utils.exceptions.telegram import (
    TelegramSendMediaGroupError,
    TelegramSendMessageError,
    TelegramSendPhotoError,
)
from utils.models import CustomMediaChunks, Post
from utils.text_sevice import chunks_to_text, correct_caption_len

logger = logging.getLogger(__name__)


async def send_news(post: Post, channel_tg_id: int, mongo: NewsRepository) -> None:
    CAPTION_LENGTH = 1024
    # TODO: Bad Request: failed to send message #1 with the error message "WEBPAGE_MEDIA_EMPTY"
    media_chunks = CustomMediaChunks(post, translate=False, convert_with_ai=True)
    media = media_chunks.get_media()
    chunks = media_chunks.get_text_chunks()
    image_link = media_chunks.get_link()

    caption = chunks_to_text(chunks)
    corrected_length_caption = correct_caption_len(caption=caption, city=post.city.ru)

    chat_id = channel_tg_id

    if media is not None:
        if len(corrected_length_caption) < CAPTION_LENGTH:
            media[0]['caption'] = corrected_length_caption
            media[0]['parse_mode'] = 'HTML'
            try:
                await send_media_group(channel_id=chat_id, media=media, post=post)
            except TelegramSendMediaGroupError as error:
                # ruff: noqa:TRY400
                logger.error(f'{error.message}')

        else:
            caption_with_embedded_image = corrected_length_caption + f'<a href="{image_link}">&#160</a>'
            try:
                await send_message(text=caption_with_embedded_image, channel_id=chat_id, post=post)
            except TelegramSendMessageError as error:
                # ruff: noqa:TRY400
                logger.error(f'{error.message}')
                try:
                    logger.info('Пробую отправить без встроенного изображения')
                    await send_message(channel_id=channel_tg_id, text=corrected_length_caption, post=post)
                except TelegramSendMessageError:
                    logger.error(f'{error.message}')
    else:
        try:
            await send_message(channel_id=channel_tg_id, text=corrected_length_caption, post=post)
        except TelegramSendMessageError as error:
            # ruff: noqa:TRY400
            logger.error(f'{error.message}')

    mongo.update_news_set_posted(news_id=post.oid)
    mongo.update_news_body_ai(news_id=post.oid, body=post.body)


async def send_message(text: str, channel_id: int, post: Post) -> None:
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage'
    data = {'chat_id': channel_id, 'text': text, 'parse_mode': 'HTML'}
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response_json = await response.json()
        if not response_json['ok']:
            raise TelegramSendMessageError(post=post, response=response_json, tg_text=text)


async def send_photo(caption: str, photo: str, channel_id: int, post: Post) -> None:
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendPhoto'
    data = {
        'chat_id': channel_id,
        'photo': photo,
        'caption': caption,
        'parse_mode': 'HTML',
    }
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response_json = await response.json()
        if not response_json['ok']:
            raise TelegramSendPhotoError(
                post=post,
                response=response_json,
                photo=photo,
                caption=caption,
            )


async def send_media_group(media: list[dict], channel_id: int, post: Post) -> None:
    url = f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMediaGroup'
    data = {'chat_id': channel_id, 'media': json.dumps(media)}
    async with aiohttp.request(method='POST', url=url, json=data) as response:
        response_json = await response.json()
        if not response_json['ok']:
            raise TelegramSendMediaGroupError(post=post, response=response_json, media=media)


if __name__ == '__main__':
    ...
