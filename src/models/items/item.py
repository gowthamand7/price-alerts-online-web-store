import re
import uuid

from bs4 import BeautifulSoup
from pip._vendor import requests

from src.common.database import Database


class Item(object):

    def __init__(self, name, price, url, store, _id = None):
        self.name = name
        self.url = url
        self.store = store
        tagname = store.tagname
        query = store.query
        self.storeId = store._id
        self.price = self.load_price(tagname, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):
        request  = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content,'html.parser')
        element = soup.find(tag_name, query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)

        return match.group()

    def saveToMongo(self):
        Database.insert(collection='items',data=self.json())

    def json(self):
        return {
            "_id":self._id,
            "name":self.name,
            "url":self.url,
            "storeId":self.storeId,
            "price":self.price
        }