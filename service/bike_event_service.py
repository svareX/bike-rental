from datetime import datetime

from database.database import get_db
from service.brand_service import BrandService


class BikeEventService():

    @staticmethod
    def rent(user_id, bike_id, date_from, date_to, total_price, payment_method):
        db = get_db()
        bike_event = 'INSERT INTO bike_events(user_id, bike_id, type, date_from, date_to, total_price, payment_method, status) VALUES(?, ?, 1, ?, ?, ?, ?, 1)'
        arguments = [user_id, bike_id, date_from, date_to, total_price, payment_method]
        db.execute(bike_event, arguments).fetchone()
        db.commit()
    @staticmethod
    def getRentDatesByID(bike_id):
        db = get_db()
        sql = 'SELECT date_from, date_to FROM bike_events WHERE bike_id=? AND status != 3'
        dates = db.execute(sql, [bike_id]).fetchone()
        return dates

    @staticmethod
    def getRentedBikesByID(user_id):
        db = get_db()
        sql = 'SELECT b.name AS bike_name, br.name AS brand_name, date_from, date_to FROM bike_events JOIN bikes b ON bike_events.bike_id = b.id JOIN brands br ON b.brand_id = br.id WHERE user_id=? AND bike_events.type = 1'
        bikes = db.execute(sql, [user_id]).fetchall()
        formatted_bikes = []
        for bike in bikes:
            formatted_bike = {
                'bike_name': bike['bike_name'],
                'brand_name': bike['brand_name'],
                'date_from': datetime.strptime(bike['date_from'], "%Y-%m-%d").strftime("%d. %m. %Y"),
                'date_to': datetime.strptime(bike['date_to'], "%Y-%m-%d").strftime("%d. %m. %Y")
            }
            formatted_bikes.append(formatted_bike)

        return formatted_bikes
    @staticmethod
    def check_rents():
        db = get_db()
        sql = 'UPDATE bike_events SET status = 2 WHERE date_to < CURRENT_DATE AND (type = 1 OR type = 2) AND status = 1'
        db.execute(sql)
        db.commit()

    @staticmethod
    def getByType(type):
        db = get_db()
        sql = '''SELECT b.id, user_id, u.first_name ||' '|| u.last_name AS user_name, b.name AS bike_name, br.name AS brand_name, date_from, date_to FROM bike_events JOIN bikes b ON bike_events.bike_id = b.id JOIN brands br ON b.brand_id = br.id JOIN users u ON user_id=u.id WHERE bike_events.status = 2 AND bike_events.type=?'''
        bikes = db.execute(sql, [type]).fetchall()
        return bikes

    @staticmethod
    def changeBikeInfo(bike_id, description, operation):
        db = get_db()
        if operation == 1:
            sql = 'UPDATE bike_events SET status = 3, description = ? WHERE status = 2 AND bike_id = ?'
        elif operation == 2:
            sql = 'UPDATE bike_events SET type = 2, description = ? WHERE status = 2 AND bike_id = ?'
        db.execute(sql, [description, bike_id])
        db.commit()


    @staticmethod
    def getAll():
        db = get_db()
        sql = '''
        SELECT bike_events.id AS id, b.name AS bike_name, brands.name AS brand_name, 
        CASE bike_events.type 
            WHEN 1 THEN 'Výpůjčka a vrácení'
            WHEN 2 THEN 'Výpůjčka -> Servis'
        END AS type, 
        CASE bike_events.status 
            WHEN 1 THEN 'Aktuálně pronajaté'
            WHEN 2 THEN 'Čeká na vyřízení'
            WHEN 3 THEN 'Vráceno/Opraveno'
        END AS status, bike_events.description AS description FROM bike_events 
        JOIN bikes b ON b.id = bike_events.bike_id 
        JOIN brands ON b.brand_id = brands.id
        '''
        bike_events = db.execute(sql).fetchall()
        return bike_events

    @staticmethod
    def getEventTypeByID(bike_id):
        db = get_db()
        sql = 'SELECT bike_events.type FROM bike_events WHERE bike_id = ? AND status = 2 ORDER BY date_to DESC LIMIT 1;'
        type = db.execute(sql, [bike_id]).fetchone()
        return type[0] if type else None

    @staticmethod
    def getByID(event_id):
        db = get_db()
        sql = '''
            SELECT bike_events.id AS id, b.name AS bike_name, brands.name AS brand_name, 
            CASE bike_events.type 
                WHEN 1 THEN 'Výpůjčka a vrácení'
                WHEN 2 THEN 'Výpůjčka -> Servis'
            END AS type, 
            CASE bike_events.status 
                WHEN 1 THEN 'Aktuálně pronajaté'
                WHEN 2 THEN 'Čeká na vyřízení'
                WHEN 3 THEN 'Vráceno/Opraveno'
            END AS status, bike_events.description AS description FROM bike_events 
            JOIN bikes b ON b.id = bike_events.bike_id 
            JOIN brands ON b.brand_id = brands.id
            WHERE bike_events.id = ?
            '''
        bike_events = db.execute(sql, [event_id]).fetchone()
        return bike_events

    @staticmethod
    def getDescriptionByBikeID(bike_id):
        db = get_db()
        sql = 'SELECT bike_events.description FROM bike_events WHERE bike_events.bike_id = ? ORDER BY date_to DESC LIMIT 1'
        description = db.execute(sql, [bike_id]).fetchone()
        return description[0] if description else None

    @staticmethod
    def deleteByBrandID(brand_id):
        db = get_db()

        delete_sql = '''
            DELETE FROM bike_events 
            WHERE bike_id IN (
                SELECT id FROM bikes 
                WHERE brand_id = ?
            )
        '''
        db.execute(delete_sql, [brand_id])
        db.commit()
