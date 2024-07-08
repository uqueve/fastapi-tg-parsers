import logging

from database.mongo.sities import get_actual_cities_json
from parsers.models.posts import Post
from utils.openai_service import OpenAIService
from utils.text_sevice import to_chunks

logger = logging.getLogger(__name__)


class CustomMediaChunks:
    def __init__(self, post: Post, translate: bool, convert_with_ai: bool):
        self.post = post
        self.title = post.title
        self.text = post.get_body()

        ai_service = OpenAIService()

        if translate:
            self.title = ai_service.translate_title_request(self.title)

        if convert_with_ai:

            try:
                language = get_actual_cities_json()[post.city_model].get('language', 'русском')
            except KeyError:
                logger.exception('Ошибка получения информации по городу')
                return
            self.text = ai_service.make_request(
                self.text, language=language, prompt_for="body",
            )
            self.title = ai_service.make_request(
                self.title, language=language, prompt_for="title",
            )

        have_post = post.images_count() > 0
        self.media = None
        self.chunks = to_chunks(self.title, self.text, first_size=4096, other_size=4096)

        if have_post:
            self.media = []

            for i in range(min(post.images_count(), 10)):
                try:
                    self.media.append(dict(type='photo', media=post.get_link(i)))
                    self.media[0]['caption'] = post.get_text()
                except Exception:
                    logger.exception('CustomMediaChunks media append error')

    def get_media(self) -> list[dict]:
        return self.media

    def get_text_chunks(self) -> [str]:
        return self.chunks

    def get_link(self) -> str:
        if self.post.images_count() > 0:
            return self.post.get_link(0)
        else:
            return 'https://img.freepik.com/free-vector/oops-404-error-with-a-broken-robot-concept-illustration_114360-5529.jpg?w=740&t=st=1708030076~exp=1708030676~hmac=869cd3aa77fc267417e08a332b3d9771539014d7879bc848221bb191b5d7dc53'
