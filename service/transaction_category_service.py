from datetime import datetime

from database.database import get_db


class TransactionCategoryService:

    @staticmethod
    def get_all():
        db = get_db()

        sql = """
            SELECT *
            FROM transaction_categories
            ORDER BY name
        """
        arguments = []

        return db.execute(sql, arguments).fetchall()
