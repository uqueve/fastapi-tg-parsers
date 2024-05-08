def to_chunks(title, text, first_size=1024, other_size=4096) -> [str]:
    title = f'<b>{title}</b>' + '\n\n'
    result = [title + text[: first_size - len(title)]]

    for i in range(first_size - len(title), len(text), other_size):
        result.append(text[i : i + other_size])

    return result


def chunks_to_text(chunks):
    caption = '\n'.join(chunks).replace('<code>', '').strip()
    caption.replace('</code>', '')
    return caption


def correct_caption_len(caption: str):
    caption = caption.split('.')
    while len(caption) > 4000:
        caption = caption.pop()

    return '\n'.join(caption)
