import hashlib
import pickle

import requests
from bs4 import BeautifulSoup
from flask import session


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
