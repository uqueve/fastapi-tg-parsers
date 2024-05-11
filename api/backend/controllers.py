import logging

from database.mongo import mongo
from utils.models import Post, PostOut

logger = logging.getLogger(__name__)


def get_unread_news(city: str | None, limit: int, offset: int) -> list[PostOut]:
    news_list = []
    news = mongo.get_unread_news(city=city, limit=limit, offset=offset)
    for new in news:
        try:
            news_obj = Post(**new)
            post_out = post_postout_adapter(post=news_obj)
            news_list.append(post_out)
        except Exception:
            logger.exception('Problem with dump models when getting unread news')
    return news_list


def post_postout_adapter(post: Post) -> PostOut:
    post_out = PostOut(
        oid=post.oid,
        title=post.title,
        body=post.body,
        image_links=post.image_links,
        date=post.date.strftime("'%d.%m.%Y %H:%M:%S"),
        link=post.link,
        city=post.city,
        posted=post.posted,
        sent=post.sent,
    )
    return post_out


def set_news_read(news_list_read: list) -> bool:
    news_read_list_of_id = []
    for news_id in news_list_read:
        news_read_list_of_id.append(news_id)
    try:
        mongo.update_news_set_read(news_read_list_of_id)
    except Exception:
        logger.exception('Error with update news status setting "read"')
        return False
    return True


def get_news_by_oid(news_oid: str) -> PostOut | None:
    new = mongo.get_news_by_oid(oid=news_oid)
    try:
        news_obj = Post(**new)
        post_out = post_postout_adapter(post=news_obj)
    except Exception:
        logger.exception('Problem with dump models when getting unread news')
        return None
    return post_out
