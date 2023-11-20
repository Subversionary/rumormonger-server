from flask import Blueprint
from .views import rumor, CreateAccount

def create_api_blueprint():
    blueprint = Blueprint('v1', __name__)
    blueprint.add_url_rule('/rumor', 'rumor', rumor, methods=['GET'])
    blueprint.add_url_rule('/create', 'create', CreateAccount)
    return blueprint
