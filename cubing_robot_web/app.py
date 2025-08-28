from flask import Flask
from flask_babel import Babel

from config import Config


babel = Babel()


def create_app() -> Flask:
    app = Flask(__name__, template_folder='app/templates', static_folder='static')
    app.config.from_object(Config)

    # Extensions
    babel.init_app(app)

    # Blueprints
    from app.controllers.main import main_bp
    from app.controllers.solving import solving_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(solving_bp)

    return app


# For WSGI servers
app = create_app()
