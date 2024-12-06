from database.database import get_db


class BikeService():

    @staticmethod
    def getAll():
        db = get_db()
        sql = '''
                    SELECT b.id, b.name, b.price_per_day, b.type, b.img, br.name AS brand_name
                    FROM bikes b
                    JOIN brands br ON b.brand_id = br.id
                '''
        bikes = db.execute(sql).fetchall()
        return bikes