from database.database import get_db


class AccountTypeService:

    @staticmethod
    def get_all():
        db = get_db()
        return db.execute(
            "SELECT * FROM account_types"
        ).fetchall()

    @staticmethod
    def get_by_id(id: int):
        db = get_db()
        return db.execute(
            "SELECT * FROM account_types WHERE id = ?",
            [id]
        ).fetchone()
