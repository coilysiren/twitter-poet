import re


def parse_text(text):
    for transform in [
        remove_links,
        remove_mentions,
        remove_special_characters,
        remove_gt,
    ]:
        text = transform(text)
    return text


def remove_mentions(string):
    return re.sub(r'@[A-Z0-9\_]*', '', string, flags=re.IGNORECASE)


def remove_links(string):
    return re.sub(r'http.*\b', '', string)


def remove_special_characters(string):
    return re.sub(r'[^\w\s]', '', string)


def remove_gt(string):
    return re.sub(r'\s*gt\s+', '', string)
