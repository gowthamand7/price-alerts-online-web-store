from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alertNeedingUpdate = Alert.findAlertsNeedUpdate()
for alert in alertNeedingUpdate:
    alert.loadItemPrice()
    alert.sendMailIfPriceReached()