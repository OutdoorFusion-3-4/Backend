
import os
from ..storage.database import Database
import os
from flask import Flask, Blueprint

db = Database()
port = int(os.getenv('PORT', 8080))

api = Blueprint('api_routes', __name__,
                template_folder='api')



app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.config['SECRET_KEY'] = str(os.getenv("JWT_TOKEN"))


def run():
    app.run(port=port, debug=True)
