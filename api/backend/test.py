import requests


# some = {'ids': [1, 2, 3, 4]}
# resp = requests.post('http://127.0.0.1:8000/news', json=some)
# print(resp.json())
# print(resp.status_code)

connection = get_mongo_connection()
# connection.create_collection('customers')
collection = connection["customers"]
print(collection.find_one())
print(collection.find_one({'name': 'John'}))
