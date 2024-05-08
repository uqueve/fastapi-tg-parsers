from bson import ObjectId
from pymongo.database import Database

from utils.models import Post, SiteModel, CitySchema


class NewsRepository:
    def __init__(self, connection):
        self.connection: Database = connection

    def get_city_by_name(self, city_name):
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('id')

    def get_city_data_by_city(self, city: str):
        collection = self.connection['cities']
        city_data = collection.find_one(filter={'name': city})
        return city_data

    def _get_all_cities(self):
        collection = self.connection['cities']
        city_data = collection.find()
        return city_data

    def get_city_tg_id_by_name(self, city_name):
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('tg_id')

    def is_news_exists_by_link(self, link):
        collection = self.connection['news']
        resp = collection.find_one(filter={'link': link})
        return bool(resp)

    def is_news_exists_by_title(self, title):
        collection = self.connection['news']
        resp = collection.find_one(filter={'title': title})
        return bool(resp)

    def add_one_news(self, post: Post):
        collection = self.connection['news']
        post_obj = post.model_dump()
        return collection.insert_one(document=post_obj).inserted_id

    def get_one_not_sent_news(self, city) -> Post | None:
        collection = self.connection['news']
        _post = collection.find_one(filter={'city.name': str(city), 'posted': False}, sort=[('date', -1)])
        if _post:
            return Post(**_post)
        else:
            return None

    def update_news_set_posted(self, news_id: str):
        collection = self.connection['news']
        collection.update_one(
            filter={'oid': news_id},
            update={'$set': {'posted': True}})

    def update_news_set_read(self, news_ids_list: list):
        collection = self.connection['news']
        collection.update_many(
            filter={"oid": {"$in": news_ids_list}},
            update={'$set': {"sent": True}})

    def update_news_body_ai(self, body, news_id):
        collection = self.connection['news']
        collection.update_one(filter={"oid": news_id}, update={'$set': {"body": body}})

    def get_unread_news(self, city: str | None):
        collection = self.connection['news']
        if not city:
            return collection.find(filter={"sent": False, "posted": True}).sort("date", -1)
        return collection.find(filter={"city.ru": city, "posted": True}).sort("date", -1)

    def get_news_by_oid(self, oid: str):
        collection = self.connection['news']
        return collection.find_one(filter={"oid": oid, "posted": True})

    def _get_one_news(self):
        collection = self.connection['news']
        return collection.find_one()

    # def _clear_collection(self, collection):
    #     collection = self.connection[collection]
    #     collection.delete_many({''})

    def _get_all_news(self):
        collection = self.connection['news']
        return collection.find()

    def _get_news_by_id(self, oid):
        collection = self.connection['news']
        return collection.find_one(filter={'oid': oid})
