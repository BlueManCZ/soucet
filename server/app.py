from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from config import ApplicationConfig
from modules.blueprints import blueprints
from modules.blueprints.tools import BlueprintInit
from modules.database.database import init_database


# Flask app initialization
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
server_session = Session(app)


# Blueprints registration
for blueprint in blueprints:
    app.register_blueprint(blueprint(BlueprintInit(bcrypt)))

# Database initialization
init_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
