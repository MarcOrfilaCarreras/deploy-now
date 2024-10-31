import hashlib
import pickle

import requests
from bs4 import BeautifulSoup
from flask import session


def detect_file_type(url: str):
    # Pls help me, this is horrible

    # Text files
    if url.endswith(".htm") or url.endswith(".html"):
        return "text/html"
    if url.endswith(".js") or url.endswith(".mjs"):
        return "text/javascript"
    if url.endswith(".css"):
        return "text/css"
    if url.endswith(".json"):
        return "text/json"
    if url.endswith(".xhtml"):
        return "application/xhtml+xml"

    # Images
    if url.endswith(".jpeg") or url.endswith(".jpg"):
        return "image/jpeg"
    if url.endswith(".png"):
        return "image/png"
    if url.endswith(".svg"):
        return "image/svg+xml"
    if url.endswith(".webp"):
        return "image/webp"
    if url.endswith(".apng"):
        return "image/apng"
    if url.endswith(".avif"):
        return "image/avif"
    if url.endswith(".gif"):
        return "image/gif"
    if url.endswith(".ico"):
        return "image/vnd.microsoft.icon"

    # Video
    if url.endswith(".avi"):
        return "video/x-msvideo"
    if url.endswith(".mp4"):
        return "video/mp4"
    if url.endswith(".webm"):
        return "video/webm"

    # Audio
    if url.endswith(".mp3") or url.endswith(".mpeg"):
        return "audio/mpeg"
    if url.endswith(".wav"):
        return "audio/wav"
    if url.endswith(".weba"):
        return "audio/webm"

    return "text/html"


def replace_url_in_tag(content: str, new_url: str, attribute: str) -> str:
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception as e:
        return content

    if new_url.endswith("/"):
        new_url = new_url[:-1]

    for tag in soup.find_all(attrs={attribute: True}):
        current_url = tag.get(attribute)

        if not current_url:
            continue

        if current_url.startswith("/"):
            tag[attribute] = new_url + current_url
            continue

        if current_url.startswith("data:"):
            continue

        if (not current_url.startswith("/")) and (not (current_url.startswith("http") or current_url.startswith("https"))):
            tag[attribute] = new_url + "/" + current_url
            continue

    return str(soup).encode('utf-8')


def replace_content(content: str, url: str) -> str:
    content = replace_url_in_tag(content, url, "href")
    content = replace_url_in_tag(content, url, "src")
    content = replace_url_in_tag(content, url, "action")

    return content


class ProxySession(object):
    def __init__(self, client: str, service: str):
        self.client = client
        self.service = service
        self.key = self.generate_key(client, service)
        self.session = requests.Session()

    @classmethod
    def generate_key(self, client: str, service: str):
        return hashlib.sha256(f"{client}_{service}".encode()).hexdigest()

    def save_session(self):
        return pickle.dumps(self.session)
