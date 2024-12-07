from database.database import get_db
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

        check_bikes = 'SELECT * FROM bikes WHERE name=? AND brand_id=?'
        bike = db.execute(check_bikes, (bikeName, bikeBrandId,)).fetchone()
        if bike:
            return {
                'error': f'Kolo s jménem "{bikeName}" a značkou "{BrandService.getNameByID(bikeBrandId)}" již existuje!'}

        sql = 'UPDATE bikes SET name = ?, price_per_day = ?, brand_id= ?, img= ? WHERE id = ?'
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
