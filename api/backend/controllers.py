import logging

from bson import ObjectId

from database.mongo import mongo
from utils.models import Post, PostOut

logger = logging.getLogger(__name__)


def get_unread_news():
    news_list = []
    news = mongo.get_unread_news()
    for new in news:
        try:
            news_obj = Post(**new)
            post_out = PostOut(
                _id=str(news_obj.id),
                title=news_obj.title,
                body=news_obj.body,
                image_links=news_obj.image_links,
                date=news_obj.date.strftime("'%d.%m.%Y %H:%M:%S"),
                link=news_obj.link
            )
            news_list.append(post_out)
        except Exception:
            logger.exception('Problem with dump models when getting unread news')
    return news_list


def set_news_read(news_list_read: list):
    news_read_list_of_objects_id = []
    for news_id in news_list_read:
        news_read_list_of_objects_id.append(ObjectId(news_id))
    try:
        mongo.update_news_set_read(news_read_list_of_objects_id)
        return True
    except Exception:
        logger.exception('Error with update news status setting "read"')
        return False
