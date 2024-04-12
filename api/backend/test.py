from collections import OrderedDict

import requests

from utils.models import CitySchema, Post

# some = {'ids': [1, 2, 3, 4]}
# resp = requests.post('http://127.0.0.1:8000/news', json=some)
# print(resp.json())
# print(resp.status_code)

# connection = get_mongo_connection()
# connection.create_collection('customers')
# collection = connection["customers"]
# print(collection.find_one())
# print(collection.find_one({'name': 'John'}))

# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, zstd',
#     'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#     'Upgrade-Insecure-Requests': '1',
# }
# asd = OrderedDict(headers)
# asd['referer'] = 'referrrrr'
# print(asd)
# content = 'seg eg seg segnsiole34ngw3 giwng lwing wingqwiopan3g vow ridsdgs;dgms;'
# print('erid' in content)

# post = Post()
# city_data = {'oid': '123', 'city': 'some_city', 'ru': 'город'}
# post.city = CitySchema(**city_data).to_dict()
# print(post.city)

some = {1,}
some.add(1)
print(type(some))