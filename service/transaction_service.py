from datetime import datetime

from click import argument

from database.database import get_db


class TransactionService:

    @staticmethod
    def get_by_id(transaction_id):
        db = get_db()
        sql = "SELECT * FROM transactions WHERE id = ?"
        arguments = [transaction_id]
        return db.execute(sql, arguments).fetchone()

    @staticmethod
    def get_all(account_id, search=None, min_amount=None):
        db = get_db()

        sql = """
            SELECT a.*, b.name as type, c.name as category 
            FROM transactions a
            JOIN transaction_types b ON a.transaction_type_id = b.id
            JOIN transaction_categories c ON a.transaction_category_id = c.id
            WHERE a.account_id = ? 
        """
        arguments = [account_id]

        if search:
            sql += " AND lower(a.description) LIKE lower(?) "
            arguments.append('%' + search + '%')

        if min_amount:
            sql += " AND a.amount >= ? "
            arguments.append(min_amount)

        sql += " ORDER BY a.date DESC "

        return db.execute(sql, arguments).fetchall()

    @staticmethod
    def insert_transaction(account_id, transaction_type, amount, category, description=None):
        db = get_db()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO transactions (account_id, transaction_type_id, amount, transaction_category_id, description, date) VALUES (?, ?, ?, ?, ?, ?)'
        arguments = [account_id, transaction_type, amount, category, description, current_datetime]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def update_transaction(transaction_id, transaction_type, amount, category, description=None):
        db = get_db()
        sql = 'UPDATE transactions SET transaction_type_id = ?, amount = ?, transaction_category_id = ?, description = ? WHERE id = ?'
        arguments = [transaction_type, amount, category, description, transaction_id]
        db.execute(sql, arguments)
        db.commit()

    @staticmethod
    def delete_transaction(transaction_id):
        db = get_db()
        sql = 'DELETE FROM transactions WHERE id = ?'
        arguments = [transaction_id]
        db.execute(sql, arguments)
        db.commit()

