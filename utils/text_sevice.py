def to_chunks(title: str, text: str, first_size: int = 1024, other_size: int = 4096) -> [str]:
    title = f'<b>{title}</b>' + '\n\n'
    result = [title + text[: first_size - len(title)]]

    for i in range(first_size - len(title), len(text), other_size):
        result.append(text[i : i + other_size])

    return result


def chunks_to_text(chunks: str) -> str:
    caption = '\n'.join(chunks).replace('<code>', '').strip()
    caption.replace('</code>', '')
    return caption


def correct_caption_len(caption: str, city: str) -> str:
    length = 4000

    city_hashtag_form = rename_city_to_hashtag_form(city)
    hashtag_text = f'\n\n#Новости{city_hashtag_form.lower()}\n#{city_hashtag_form}'

    split_caption = caption.split('.')
    while len(caption) + len(hashtag_text) > length:
        split_caption.pop()
        caption = '\n'.join(split_caption)
    return caption + hashtag_text


def rename_city_to_hashtag_form(city: str) -> str:
    return city.replace(' ', '').replace('-', '')
