from database.database import get_db


class AccountService:

    @staticmethod
    def get_all(account_type_id = None,):
        db = get_db()

        sql = "SELECT * FROM accounts "
        arguments = []

        if account_type_id is not None:
            sql += " WHERE account_type_id = ? "
            arguments.append(account_type_id)

        return db.execute(sql, arguments).fetchall()
