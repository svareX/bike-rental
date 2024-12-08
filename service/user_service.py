import hashlib

from database.database import get_db
import config

class UserService():
  
    @staticmethod
    def verify(email, password):
        db = get_db()
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())

        sql = '''
            SELECT u.id, u.first_name, u.last_name, u.email, u.role 
            FROM users u
            WHERE u.email = ? AND u.password = ?   
        '''
        arguments = [email, hashed_password.hexdigest()]

        user = db.execute(sql, arguments).fetchone()

        return user if user else None
    @staticmethod
    def register(first_name, last_name, email, password):
        db = get_db()
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode()).hexdigest()

        check_user_sql = "SELECT * FROM users WHERE email = ?"
        user = db.execute(check_user_sql, [email]).fetchone()

        if user:
            return user

        insert_user_sql = """
        INSERT INTO users (first_name, last_name, email, password, role, created_at, updated_at)
        VALUES (?, ?, ?, ?, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        db.execute(insert_user_sql, [first_name, last_name, email, hashed_password])
        db.commit()

    @staticmethod
    def getByID(user_id):
        db = get_db()
        sql = "SELECT * FROM users WHERE id = ?"
        user = db.execute(sql, [user_id]).fetchone()
        return user
