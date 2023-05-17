import os.path
import requests
from bs4 import BeautifulSoup as BS


class Mirea:
    url = 'https://student.mirea.ru/ads/?PAGEN_1=1'
    lastkey = ""
    lastkey_file = ""

    def __init__(self, lastkey_file):
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def new_news(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        new = []
        items = html.select('main > div.container.g-pt-20.g-pb-50 .g-mb-30 > a')
        key = items[0].get('href')
        if self.lastkey < key:
            new.append(key)

        return new

    def news_info(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        # form data
        info = {
            "id": html.select('main > div.container.g-pt-20.g-pb-50 .g-mb-30 > a')[0].get('href'),
            "tittle": html.select('main > div.container.g-pt-20.g-pb-50 .g-mb-35 > h3')[0].text,
            "link": "https://student.mirea.ru" + html.select('main > div.container.g-pt-20.g-pb-50 .g-mb-30 > a')[
                0].get('href'),
            "image": "photo",
            "text": html.select("main > div.container.g-pt-20.g-pb-50 .g-mb-35 > p")[0].text
        }

        return info

    def get_lastkey(self):
        r = requests.get(self.url)
        html = BS(r.content, 'html.parser')

        items = html.select('main > div.container.g-pt-20.g-pb-50 .g-mb-30 > a')
        return items[0].get('href')

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, "r+") as f:
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key
