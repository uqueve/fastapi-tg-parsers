from bson import ObjectId
from pymongo.database import Database

from utils.models import Post


class NewsRepository:
    def __init__(self, connection):
        self.connection: Database = connection

    def get_city_by_name(self, city_name):
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('id')

    def get_city_tg_id_by_name(self, city_name):
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('tg_id')

    def is_news_exists_by_link(self, link):
        collection = self.connection['news']
        resp = collection.find_one(filter={'link': link})
        return bool(resp)

    def add_one_news(self, post: Post):
        collection = self.connection['news']
        post_obj = post.model_dump()
        return collection.insert_one(document=post_obj).inserted_id

    def get_one_not_sent_news(self, city) -> Post | None:
        collection = self.connection['news']
        _post = collection.find_one(filter={'city': city, 'posted': False})
        if _post:
            return Post(**_post)
        else:
            return None

    def update_news_set_posted(self, news_id: str):
        collection = self.connection['news']
        collection.update_one(
            filter={'_id': ObjectId(news_id)},
            update={'$set': {'posted': True}})

    def update_news_set_read(self, news_ids_list: list):
        collection = self.connection['news']
        collection.update_many(
            filter={"_id": {"$in": news_ids_list}},
            update={'$set': {"sent": True}})

    def update_news_body_ai(self, body, news_id):
        collection = self.connection['news']
        collection.update_one(filter={"_id": news_id}, update={'$set': {"body": body}})

    def get_unread_news(self):
        collection = self.connection['news']
        return collection.find(filter={"sent": False, "posted": True})

    def _get_one_news(self):
        collection = self.connection['news']
        return collection.find_one()

    # def _clear_collection(self, collection):
    #     collection = self.connection[collection]
    #     collection.delete_many({''})

    def _get_all_news(self):
        collection = self.connection['news']
        return collection.find()

    def _get_news_by_id(self, _id):
        collection = self.connection['news']
        return collection.find_one(filter={'_id': ObjectId(_id)})
