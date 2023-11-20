import configparser

config = configparser.ConfigParser()

config['OpenAI'] = {
    'API_KEY': '',
    'API_ENDPOINT': '',
    'MODEL': '',
    'TOKENLIMIT': ''
}

config['API'] = {
    'RATELIMIT': '',
    'OPENREGISTRATION': ''
}

config['RUMOR'] = {
    'SECRET': ''
}


def save():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def load():
    with open('config.ini', 'r') as configfile:
        config.read("config.ini")
