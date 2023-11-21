from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .views import rumor, CreateAccount
from config import config

limiter = Limiter(key_func=get_remote_address)


def create_api_blueprint():
    blueprint = Blueprint('v1', __name__)

    ratelimit = config['API']['ratelimit']

    rumor_view = limiter.limit(f"{ratelimit} per minute")(rumor)

    blueprint.add_url_rule('/rumor', 'rumor', rumor_view, methods=['GET'])
    blueprint.add_url_rule('/create', 'create', CreateAccount)
    return blueprint
