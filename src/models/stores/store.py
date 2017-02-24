import uuid

from src.common.database import Database
import src.models.stores.errors as storeErrors

class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store :: {}>".format(self.name)

    def save_to_mongo(self):
        Database.insert(collection='stores', data=self.json())

    @classmethod
    def get_by_id(cls, id):
        store = Database.findOne(collection='stores', query={"_id": id})
        if store is not None:
            return cls(**store)

    @classmethod
    def get_by_name(cls, name):
        store = Database.findOne(collection='stores', query={"name": name})
        if store is not None:
            return cls(**store)

    @classmethod
    def get_by_url_prefix(cls, url_prefix):

        store = Database.findOne(collection='stores', query={"url_prefix": {"$regex": '^{}'.format(url_prefix)}})
        if store is not None:
            return cls(**store)

    @classmethod
    def find_by_url(cls, url):
        for i in range(0, len(url)+1):
            store = cls.get_by_url_prefix(url[:i])
            if store is not None:
                return store
            else:
                raise storeErrors.StoreNotFound("No store found for the given url !", 404)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }