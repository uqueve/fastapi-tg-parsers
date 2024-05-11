import datetime

from pymongo.cursor import Cursor
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult

from utils.models import Post, SiteModel


class NewsRepository:
    def __init__(self, connection: Database):
        self.connection: Database = connection

    def get_city_by_name(self, city_name: str) -> int:
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('id')

    def get_city_data_by_city(self, city: str) -> dict:
        collection = self.connection['cities']
        city_data = collection.find_one(filter={'name': city})
        return city_data

    def _get_all_cities(self) -> Cursor:
        collection = self.connection['cities']
        city_data = collection.find()
        return city_data

    def get_city_tg_id_by_name(self, city_name: str) -> int:
        collection = self.connection['cities']
        city = collection.find_one(filter={'name': city_name})
        return city.get('tg_id')

    def is_news_exists_by_link(self, link: str) -> bool:
        collection = self.connection['news']
        resp = collection.find_one(filter={'link': link})
        return bool(resp)

    def is_news_exists_by_title(self, title: str) -> bool:
        collection = self.connection['news']
        resp = collection.find_one(filter={'title': title})
        return bool(resp)

    def add_one_news(self, post: Post) -> InsertOneResult:
        collection = self.connection['news']
        post_obj = post.model_dump()
        return collection.insert_one(document=post_obj).inserted_id

    def get_one_not_sent_news(self, city: SiteModel) -> Post | None:
        collection = self.connection['news']
        _post = collection.find_one(
            filter={'city.name': str(city), 'posted': False},
            sort=[('date', -1)],
        )
        if _post:
            return Post(**_post)
        else:
            return None

    def update_news_set_posted(self, news_id: str) -> UpdateResult:
        collection = self.connection['news']
        return collection.update_one(
            filter={'oid': news_id},
            update={'$set': {'posted': True}},
        )

    def update_news_set_read(self, news_ids_list: list) -> UpdateResult:
        collection = self.connection['news']
        return collection.update_many(
            filter={'oid': {'$in': news_ids_list}},
            update={'$set': {'sent': True}},
        )

    def update_news_body_ai(self, body: str, news_id: str) -> UpdateResult:
        collection = self.connection['news']
        return collection.update_one(filter={'oid': news_id}, update={'$set': {'body': body}})

    def get_unread_news(self, city: str | None, limit: int, offset: int) -> Cursor:
        collection = self.connection['news']
        if not city:
            return collection.find(filter={'sent': False, 'posted': True}).sort('date', -1).skip(offset).limit(limit)
        return collection.find(filter={'city.ru': city, 'posted': True}).sort('date', -1).skip(offset).limit(limit)

    def get_news_by_oid(self, oid: str) -> dict:
        collection = self.connection['news']
        return collection.find_one(filter={'oid': oid, 'posted': True})

    def clear_not_posted_news_by_date(self, date: datetime.datetime):
        collection = self.connection['news']
        return collection.delete_many(filter={'date': {'$lt': date}, 'posted': False})

    def _get_one_news(self) -> dict:
        collection = self.connection['news']
        return collection.find_one()

    # def _clear_collection(self, collection):
    #     collection = self.connection[collection]
    #     collection.delete_many({''})

    def _get_all_news(self) -> Cursor:
        collection = self.connection['news']
        return collection.find()

    def _get_news_by_id(self, oid: str) -> dict:
        collection = self.connection['news']
        return collection.find_one(filter={'oid': oid})
