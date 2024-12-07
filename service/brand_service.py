from database.database import get_db


class BrandService():
    @staticmethod
    def getAll():
        db = get_db()
        sql = ''' SELECT id, name FROM brands
        '''
        brands = db.execute(sql).fetchall()
        return brands

    @staticmethod
    def getNameByID(brandId):
        db = get_db()
        sql = ''' SELECT
        name FROM brands WHERE id=?
        '''
        brands = db.execute(sql, brandId).fetchone()
        return brands[0]