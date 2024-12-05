from datetime import datetime

from database.database import get_db


class TransactionTypeService:

    @staticmethod
    def get_all():
        db = get_db()

        sql = """
            SELECT *
            FROM transaction_types
            ORDER BY name
        """
        arguments = []

        return db.execute(sql, arguments).fetchall()
