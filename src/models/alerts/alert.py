import uuid
import datetime

from pip._vendor import requests

from src.common.database import Database
from src.models.alerts import constants as alertConstants
from src.models.items.item import Item


class Alert(object):

    def __init__(self, userEmail, price_limit, itemId, lastChecked=None, _id=None):
        self.userEmail = userEmail
        self.price_limit = price_limit
        self.item = Item.getById(itemId)
        self.lastChecked = datetime.datetime.utcnow() if lastChecked is None else lastChecked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {} >".format(self.userEmail,self.item.name,self.price_limit)

    def send(self):
        return requests.post(
            alertConstants.URL,
            auth= ("api", alertConstants.APIKEY),
            data= {"from": alertConstants.FROM,
                  "to": self.userEmail,
                  "subject": "Price limit reached for {}".format(self.item.name),
                  "text": "We found a deal (link here)"})


    @classmethod
    def findAlertsNeedUpdate(cls,intervel= alertConstants.AlertIntervel):
        lastUpdatedLimit = datetime.datetime.utcnow() - datetime.timedelta(seconds=intervel)
        return [cls(**elem) for elem in Database.find(collection= 'alerts',query={"lastChecked" :
                                                                                    {"$gte": lastUpdatedLimit}
                                                                            })]

    def save_to_mongo(self):
        Database.insert(collection='alerts',data=self.json())

    def loadItemPrice(self):
        self.item.load_price()
        self.save_to_mongo()
        return self.item.price

    def sendMailIfPriceReached(self):
        if self.item.price < self.price_limit:
            self.send()

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "lastChecked": self.lastChecked  ,
            "userEmail": self.userEmail,
            "itemId": self.item._id
        }