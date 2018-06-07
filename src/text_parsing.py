import re


def parse_text(text):
    for transform in [
        remove_RTs,
        remove_links,
        remove_mentions,
        remove_special_characters,
    ]:
        text = transform(text)
    return text


def remove_RTs(string):
    return re.sub(r'\bRT\b', '', string, flags=re.IGNORECASE)


def remove_mentions(string):
    return re.sub(r'@[A-Z0-9\_]*', '', string, flags=re.IGNORECASE)


def remove_links(string):
    return re.sub(r'http.*\b', '', string)


def remove_special_characters(string):
    return re.sub(r'[:\?\=\&\(\)\!\;\^]', '', string)
