from flask import Flask

from ChatGPT.rumormonger import Rumormonger
from Database.Rumors import Rumors
from v1 import create_api_blueprint
import config

app = Flask(__name__)

# Register the API blueprint
api_blueprint = create_api_blueprint()
app.register_blueprint(api_blueprint, url_prefix='/v1')


def run_app():
    config.load()
    Rumors.initialize_db()
    Rumormonger.init()
    app.run(debug=True)


if __name__ == '__main__':
    run_app()
