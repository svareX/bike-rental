from database.database import get_db
from service.bike_event_service import BikeEventService
from service.brand_service import BrandService


class BikeService():

    @staticmethod
    def getAll():
        db = get_db()
        sql = '''
                    SELECT b.id, b.name, b.price_per_day, b.type, b.img, br.name AS brand_name, br.id AS bike_brand_id
                    FROM bikes b
                    JOIN brands br ON b.brand_id = br.id
                '''
        bikes = db.execute(sql).fetchall()
        return bikes

    @staticmethod
    def add(bikeName, bikeBrand_id, bikePrice_per_day, bikeImg):
        db = get_db()

        check_bikes = 'SELECT * FROM bikes WHERE name=? AND brand_id=?'
        bike = db.execute(check_bikes, (bikeName,bikeBrand_id,)).fetchone()
        if bike:
            return {'error': f'Kolo s jménem "{bikeName}" a značkou "{BrandService.getNameByID(bikeBrand_id)}" již existuje!'}


        sql = 'INSERT INTO bikes (name, brand_id, type, price_per_day, img) VALUES (?, ?, 0, ?, ?)'
        arguments = [bikeName, bikeBrand_id, bikePrice_per_day, bikeImg]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def getByID(bike_id):
        db = get_db()
        sql = 'SELECT b.id, b.name, b.price_per_day, b.brand_id, b.img, br.name AS brand_name FROM bikes b JOIN brands br ON br.id=brand_id WHERE b.id=?'
        arguments = [bike_id]
        bike = db.execute(sql, arguments).fetchone()
        return bike

    @staticmethod
    def update(bikeID, bikeName, bikePricePerDay, bikeBrandId, bikeImg):
        db = get_db()

        current_bike = db.execute('SELECT * FROM bikes WHERE id = ?', (bikeID,)).fetchone()

        if current_bike['name'] != bikeName or current_bike['brand_id'] != bikeBrandId:
            check_bikes = 'SELECT * FROM bikes WHERE name=? AND brand_id=? AND id != ?'
            bike = db.execute(check_bikes, (bikeName, bikeBrandId, bikeID)).fetchone()
            if bike:
                return {
                    'error': f'Kolo s jménem "{bikeName}" a značkou "{BrandService.getNameByID(bikeBrandId)}" již existuje!'}

        sql = 'UPDATE bikes SET name = ?, price_per_day = ?, brand_id = ?, img = ? WHERE id = ?'
        arguments = [bikeName, bikePricePerDay, bikeBrandId, bikeImg, bikeID]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def deleteByID(bikeID):
        db = get_db()
        sql = 'DELETE FROM bikes WHERE id=?'
        arguments = [bikeID]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def getStatus(bike_id):
        db = get_db()
        sql = '''
            SELECT status 
            FROM bike_events 
            WHERE bike_id = ? 
              AND (type = 1 OR type = 2) -- Group type conditions
            ORDER BY date_to DESC 
            LIMIT 1
        '''
        rented = db.execute(sql, [bike_id]).fetchone()
        return rented['status'] if rented else 0
    @staticmethod
    def getByBrand(brand_id):
        db = get_db()
        sql = '''
            SELECT b.id, b.name, b.price_per_day, b.type, b.img, br.name AS brand_name, br.id AS bike_brand_id
            FROM bikes b
            JOIN brands br ON b.brand_id = br.id
            WHERE br.id = ?
        '''
        bikes = db.execute(sql, [brand_id]).fetchall()
        return bikes

    @staticmethod
    def getByBrandAndSearch(brand_id, search_query):
        db = get_db()
        sql = '''
            SELECT b.id, b.name, b.price_per_day, b.type, b.img, br.name AS brand_name, br.id AS bike_brand_id
            FROM bikes b
            JOIN brands br ON b.brand_id = br.id
            WHERE br.id = ? AND b.name LIKE ?
        '''
        bikes = db.execute(sql, [brand_id, f"%{search_query}%"]).fetchall()
        return bikes

    @staticmethod
    def getBySearch(search_query):
        db = get_db()
        sql = '''
            SELECT b.id, b.name, b.price_per_day, b.type, b.img, br.name AS brand_name, br.id AS bike_brand_id
            FROM bikes b
            JOIN brands br ON b.brand_id = br.id
            WHERE b.name LIKE ?
        '''
        bikes = db.execute(sql, [f"%{search_query}%"]).fetchall()
        return bikes

    @staticmethod
    def getBikesFiltered(brand_id=None, search_query=None, rent_status=None):
        db = get_db()

        query = '''
        SELECT DISTINCT bikes.*, brands.name AS brand_name
        FROM bikes
        LEFT JOIN (
            SELECT bike_id, status
            FROM bike_events
            WHERE date_to = (
                SELECT MAX(date_to)
                FROM bike_events AS sub
                WHERE sub.bike_id = bike_events.bike_id
            )
        ) AS latest_event ON bikes.id = latest_event.bike_id
        LEFT JOIN brands ON bikes.brand_id = brands.id
        WHERE 1=1
        '''
        params = []

        if brand_id and brand_id.isdigit():
            query += " AND bikes.brand_id = ?"
            params.append(brand_id)

        if search_query:
            query += " AND bikes.name LIKE ?"
            params.append(f"%{search_query}%")

        if rent_status == "free":
            query += " AND (latest_event.bike_id IS NULL OR latest_event.status = 3)"
        elif rent_status == "rented":
            query += " AND latest_event.status IN (1, 2)"

        bikes = db.execute(query, params).fetchall()
        return bikes

    @staticmethod
    def deleteByBrand(brand_id):
        db = get_db()
        sql = 'DELETE FROM bikes WHERE brand_id=?'
        arguments = [brand_id]
        db.execute(sql, arguments)
        db.commit()
