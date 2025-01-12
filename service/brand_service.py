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

    @staticmethod
    def add(brand_name):
        db = get_db()
        sql = '''
        SELECT * FROM brands WHERE name=?
        '''
        brand = db.execute(sql, [brand_name]).fetchone()
        if brand:
            return 0
        else:
            sql = '''
            INSERT INTO brands (name) VALUES (?)'''
            brand = db.execute(sql, [brand_name])
            db.commit()

    @staticmethod
    def getIDByName(brand_name):
        db = get_db()
        sql = '''
        SELECT id FROM brands WHERE name=?
        '''
        brand_id = db.execute(sql, [brand_name]).fetchone()
        return brand_id[0]

    @staticmethod
    def delete(brand_id):
        db = get_db()
        sql = '''
        DELETE FROM brands WHERE id=?
        '''
        db.execute(sql, [brand_id])
        db.commit()