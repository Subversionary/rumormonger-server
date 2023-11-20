from Database.Rumors import Rumors

class Account:
    def __init__(self, key, tokens, ip, banned):
        self._key = key
        self._tokens = tokens
        self._ip = ip
        self._banned = banned

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        Rumors.update_data(self._key, self._tokens, self._ip, self._banned)

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        self._tokens = value
        Rumors.update_data(self._key, self._tokens, self._ip, self._banned)

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value
        Rumors.update_data(self._key, self._tokens, self._ip, self._banned)

    @property
    def banned(self):
        return self._banned

    @banned.setter
    def banned(self, value):
        self._banned = value
        Rumors.update_data(self._key, self._tokens, self._ip, self._banned)
