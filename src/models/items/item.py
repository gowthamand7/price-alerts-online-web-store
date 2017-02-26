import re
import uuid

from bs4 import BeautifulSoup
from pip._vendor import requests

from src.common.database import Database
from src.models.stores.store import Store


class Item(object):

    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tagname = store.tag_name
        self.query = store.query
        self.price = None
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content,'html.parser')
        element = soup.find(self.tagname, self.query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = match.group()
        return self.price

    @classmethod
    def getById(cls,Id):
        return cls(**Database.findOne(collection='item',query={"_id":Id}))

    def save_to_mongo(self):
        Database.insert(collection='items',data=self.json())

    def json(self):
        return {
            "_id":self._id,
            "name":self.name,
            "url":self.url
        }