import hashlib
from symbol import argument

from database.database import get_db
import config

class UserService():
  
    @staticmethod
    def verify(login, password):
        db = get_db()
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        # print(hashed_password.hexdigest())

        sql = '''
            SELECT u.id, u.name, u.login, r.role 
            FROM users u
            JOIN user_roles r ON u.user_role_id = r.id
            WHERE u.login = ? AND u.password = ?
        '''
        arguments = [login, hashed_password.hexdigest()]

        user = db.execute(sql, arguments).fetchone()

        return user if user else None
