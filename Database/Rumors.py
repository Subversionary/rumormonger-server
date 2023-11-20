import sqlite3


class Rumors:
    __conn = None

    @classmethod
    def initialize_db(cls):
        cls.__conn = sqlite3.connect('rumors.db')
        cls.check_create_table()
        cls.__conn.close()

    @staticmethod
    def get_db_connection():
        return sqlite3.connect('rumors.db', check_same_thread=False)

    @classmethod
    def check_create_table(cls):
        cursor = cls.__conn.cursor()
        cursor.execute('''
CREATE TABLE IF NOT EXISTS rumors (
    key TEXT UNIQUE,
    tokens INT,
    lastip TEXT,
    banned INTEGER DEFAULT 0
)
''')
        cls.__conn.commit()

    @classmethod
    def insert_data(cls, key_value, tokens_value, lastip_value, banned_value=False):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
INSERT INTO rumors (key, tokens, lastip, banned) VALUES (?, ?, ?, ?)
''', (key_value, tokens_value, lastip_value, banned_value))
        conn.commit()

    @classmethod
    def update_data(cls, key_value, tokens_value, lastip_value, banned_value):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
UPDATE rumors SET tokens = ?, lastip = ?, banned = ? WHERE key = ?
''', (tokens_value, lastip_value, banned_value, key_value))
        conn.commit()

    @classmethod
    def get_data_by_key(cls, key_value):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
SELECT key, tokens, lastip, banned FROM rumors WHERE key = ?
''', (key_value,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {'key': row[0], 'tokens': row[1], 'lastip': row[2], 'banned': bool(row[3])}
        return None

    @classmethod
    def is_key_banned(cls, key_value):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
SELECT banned FROM rumors WHERE key = ?
''', (key_value,))
        row = cursor.fetchone()
        conn.close()
        return bool(row[0]) if row else False
