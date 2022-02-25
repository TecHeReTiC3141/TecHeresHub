import sqlite3
import time
from werkzeug.security import generate_password_hash, check_password_hash


class UDataBase:

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.cur = db.cursor()

    def get_users(self):
        try:
            res = self.cur.execute('''SELECT * FROM users_score 
            ORDER BY score DESC;''')
            if res:
                return res
        except Exception:
            print('Error with database')
            return self.cur.execute('''SHOW TABLES''')
        return []

    def add_post(self, author, title, text):
        try:
            t = round(time.time())
            self.cur.execute('''INSERT INTO users_posts (author, title, text, time) 
            VALUES (?, ?, ?, ?)''', (author, title, text, t))
            self.db.commit()
        except sqlite3.Error as e:
            print(e)
            return False
        return True

    def get_posts(self):
        try:
            self.cur.execute('''SELECT * FROM users_posts 
            ORDER BY time DESC''')
            res = self.cur.fetchall()
            if res:
                return res
        except sqlite3.Error:
            print('Error with database')
        return []

    def get_post(self, id):
        try:
            self.cur.execute('''SELECT * FROM users_posts 
            WHERE id = ?''', (id))
            res = self.cur.fetchone()
            if res:
                return res
        except sqlite3.Error:
            print('Error with database')
        return None

    def add_user(self, email, name, password):
        user_emails = self.cur.execute('''SELECT * 
        FROM users_score WHERE mail = ?''', [email]).fetchall()
        print(user_emails)
        if user_emails:
            return False
        self.cur.execute('''INSERT INTO users_score (name, mail, password) 
        VALUES (?, ?, ?)''', (name, email, password))
        self.db.commit()
        return True

    def check_login(self, email, password):
        user_info = self.cur.execute('''SELECT *
        FROM users_score WHERE mail = ?''', (email,)).fetchone()
        if user_info is None:
            return False
        print(password)
        return check_password_hash(user_info['password'], password), user_info['name']

    def show_users_posts(self, user_name):
        users_posts = self.cur.execute('''SELECT title, visited FROM users_posts
                                            WHERE author = ?
                                            ORDER BY visited DESC''', (user_name,))
        return users_posts

    def top_users(self):
        pass

