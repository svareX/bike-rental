import hashlib

from database.database import get_db
import config

class UserService():
  
    @staticmethod
    def verify(email, password):
        db = get_db()
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())

        sql = '''
            SELECT u.id, u.first_name, u.last_name, u.email, u.role, u.avatar 
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

    #Metoda, která zjišťuje spolehlivost uživatele (kola vrácená v dobrém stavu/všechna vrácená kola)
    @staticmethod
    def getReliability(user_id):
        db = get_db()
        sql = '''
        SELECT COUNT(user_id) FROM bike_events 
        WHERE user_id=? AND type = 1
        '''
        good_condition_bikes = db.execute(sql, [user_id]).fetchone()[0]

        sql = '''
        SELECT COUNT(user_id) FROM bike_events WHERE user_id=?
        '''
        all_bikes = db.execute(sql, [user_id]).fetchone()[0]

        if all_bikes == 0:  # Ochrana proti dělení nulou
            return all_bikes, good_condition_bikes, 0

        reliability = round((good_condition_bikes / all_bikes) * 100, 2)
        return all_bikes, good_condition_bikes, reliability

    @staticmethod
    def changeName(user_id, new_first_name, new_last_name):
        db = get_db()
        sql = '''
        UPDATE users SET first_name=?, last_name=? WHERE id=?
        '''
        db.execute(sql, [new_first_name, new_last_name, user_id])
        db.commit()
    @staticmethod
    def changeEmail(user_id, email):
        db = get_db()

        sql = '''
        SELECT email FROM users WHERE email=?
        '''
        user = db.execute(sql, [email]).fetchone()
        if user is None:
            sql = '''
            UPDATE users SET email=? WHERE id=?
            '''
            db.execute(sql, [email, user_id])
            db.commit()
            return True
        else:
            return False

    @staticmethod
    def changeAvatar(user_id, avatar_url):
        db = get_db()
        sql = '''
        UPDATE users SET avatar=? WHERE id=?
        '''
        db.execute(sql, [avatar_url, user_id])
        db.commit()
