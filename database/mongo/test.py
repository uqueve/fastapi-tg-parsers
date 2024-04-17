from bson import ObjectId

from api.backend.controllers import get_unread_news
# from database.mongo import mongo
# from utils.models import Post
#
# post = Post(
#     title='Some title 55',
#     body='Some body 55',
#     image_links=['link 1', 'link 2']
# )
# news_id = mongo.add_one_news(post=post)
# print(news_id)
# mongo.update_news_body_ai(news_id=news_id, body='Some new body!')
# print(mongo._get_news_by_id(_id=news_id))

# post = mongo._get_news_by_id('6600779adb0598ff63f14f26')
# print(post)
# post = Post(**post)
# print(post.id)
# post = mongo._get_one_news()
# print(post)
# post = Post(**post)
# print(post)
# print(Post(**post))
# post = Post(title=None)
# news = mongo.get_unread_news()
# news = mongo._get_all_news()
# news = get_unread_news()
# news = mongo._get_one_news()
# news = Post(**news)
# print(str(news.id))
# news = get_unread_news()
# print()
# print(news)
# news_list = []
# for new in news:
#     news_obj = Post(**new)
#     news_list.append(news_obj)
    # print(new)
# print(news_list)
# print('\n\n')

# news_unread_ids = [ObjectId('66006fb402ac01513b1c4765'), ObjectId('66007661cc1e28a9a840ec8f'), ObjectId('660076b45d07fb2db8305ec2')]
# mongo.update_news_set_read(news_unread_ids)
#
# news = mongo._get_all_news()
# for new in news:
#     print(new.get('_id'))
#     print(new.get('read'))
