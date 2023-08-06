import logging
from urllib import parse

host = 'youtube.com'


def yt_music_link_to_yt_link(input_url: str) -> str:
    url_parts = list(parse.urlparse(input_url))
    url_parts[1] = host
    return parse.urlunparse(url_parts)
