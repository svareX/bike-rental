from database.database import get_db


class StatisticsService():
    @staticmethod
    def getUserCount():
        db = get_db()
        sql = 'SELECT COUNT(*) FROM users'
        count = db.execute(sql).fetchone()
        return count[0]

    @staticmethod
    def getTotalBikeRevenue():
        db = get_db()
        sql = 'SELECT SUM(total_price) FROM bike_events'
        revenue = db.execute(sql).fetchone()
        return revenue[0]

    @staticmethod
    def getMostRentedBike():
        db = get_db()
        sql = 'SELECT bikes.name FROM bike_events JOIN bikes ON bike_events.bike_id = bikes.id GROUP BY bike_id ORDER BY COUNT(bike_id) DESC LIMIT 1'
        bike = db.execute(sql).fetchone()
        return bike[0]

    @staticmethod
    def getMostRentedBrand():
        db = get_db()
        sql = 'SELECT brands.name FROM bike_events JOIN bikes ON bike_events.bike_id = bikes.id JOIN brands ON bikes.brand_id = brands.id GROUP BY bike_id ORDER BY COUNT(bike_id) DESC'
        brand = db.execute(sql).fetchone()
        return brand[0]

    @staticmethod
    def getTotalNumberOfRents():
        db = get_db()
        sql = 'SELECT COUNT(*) FROM bike_events'
        rents = db.execute(sql).fetchone()
        return rents[0]

    @staticmethod
    def getBrandRents():
        db = get_db()
        sql = 'SELECT COUNT(brands.id), brands.name FROM bike_events JOIN bikes ON bike_events.bike_id = bikes.id JOIN brands ON bikes.brand_id = brands.id GROUP BY brands.id ORDER BY COUNT(brands.id) DESC'
        brand_rents = db.execute(sql).fetchall()
        return brand_rents