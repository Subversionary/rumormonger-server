import sqlite3

class Rumors:
    DATABASE = 'rumors.db'

    @staticmethod
    def execute_query(query, params=None, commit=False, fetchone=False):
        with sqlite3.connect(Rumors.DATABASE, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            return cursor.fetchall() if query.strip().upper().startswith('SELECT') else None

    @classmethod
    def initialize_db(cls):
        cls.execute_query('''
            CREATE TABLE IF NOT EXISTS rumors (
                key TEXT UNIQUE,
                tokens INT,
                lastip TEXT,
                banned INTEGER DEFAULT 0
            )
        ''', commit=True)

    @classmethod
    def insert_data(cls, key_value, tokens_value, lastip_value, banned_value=False):
        cls.execute_query('''
            INSERT INTO rumors (key, tokens, lastip, banned) VALUES (?, ?, ?, ?)
        ''', (key_value, tokens_value, lastip_value, banned_value), commit=True)

    @classmethod
    def update_data(cls, key_value, tokens_value, lastip_value, banned_value):
        """
        Updates row by key
        """
        cls.execute_query('''
            UPDATE rumors SET tokens = ?, lastip = ?, banned = ? WHERE key = ?
        ''', (tokens_value, lastip_value, banned_value, key_value), commit=True)

    @classmethod
    def get_data_by_key(cls, key_value):
        """
        Retrieves a row by key
        :param key_value: key/token value
        :return: Row with key, if none found - None
        """
        row = cls.execute_query('''
            SELECT key, tokens, lastip, banned FROM rumors WHERE key = ?
        ''', (key_value,), fetchone=True)
        return {'key': row[0], 'tokens': row[1], 'lastip': row[2], 'banned': bool(row[3])} if row else None

    @classmethod
    def is_key_banned(cls, key_value):
        """
        Checks if a key is banned
        :param key_value: key/token value
        :return: True is banned, otherwise False.
        """
        row = cls.execute_query('''
            SELECT banned FROM rumors WHERE key = ?
        ''', (key_value,), fetchone=True)
        return bool(row[0]) if row else False
