from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Fügen Sie die max- und min-Funktionen zur Jinja2-Umgebung hinzu
    app.jinja_env.globals.update(max=max, min=min)
    
    return app