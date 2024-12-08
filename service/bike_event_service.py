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
    @staticmethod
    def getRentEndDateByID(bike_id):
        db = get_db()
        sql = 'SELECT date_to FROM bike_events WHERE bike_id=?'
        bike = db.execute(sql, [bike_id]).fetchone()

        date_obj = datetime.strptime(bike['date_to'], '%Y-%m-%d')
        return date_obj.strftime("%d. %m. %Y")

    @staticmethod
    def getRentedBikesByID(user_id):
        db = get_db()
        sql = 'SELECT b.name AS bike_name, br.name AS brand_name, date_from, date_to FROM bike_events JOIN bikes b ON bike_events.bike_id = b.id JOIN brands br ON b.brand_id = br.id WHERE user_id=? AND bike_events.type = 0'
        bikes = db.execute(sql, [user_id]).fetchall()
        formatted_bikes = []
        for bike in bikes:
            formatted_bike = {
                'bike_name': bike['bike_name'],
                'brand_name': bike['brand_name'],
                'date_from': datetime.strptime(bike['date_from'], "%Y-%m-%d").strftime("%d. %m. %Y"),
                # Example: 12.06.2024
                'date_to': datetime.strptime(bike['date_to'], "%Y-%m-%d").strftime("%d. %m. %Y")
            }
            formatted_bikes.append(formatted_bike)

        return formatted_bikes
