from datetime import datetime

from database.database import get_db
from service.brand_service import BrandService


class BikeEventService():

    @staticmethod
    def rent(user_id, bike_id, date_from, date_to):
        db = get_db()
        bike_event = 'INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to) VALUES(?, ?, 0, ?, ?)'
        arguments = [user_id, bike_id, date_from, date_to]
        db.execute(bike_event, arguments).fetchone()
        db.commit()
    def getRentEndDateByID(bike_id):
        db = get_db()
        sql = 'SELECT date_to FROM bike_events WHERE bike_id=?'
        bike = db.execute(sql, [bike_id]).fetchone()

        date_obj = datetime.strptime(bike['date_to'], '%Y-%m-%d')
        return date_obj.strftime("%d. %m. %Y")

