from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS  # flask_cors modülünü içe aktarın

from datetime import timedelta

from internify.models import *
from internify.jwt_token import jwt
from internify.auth.urls import bp as auth_bp
from internify.student.urls import bp as student_bp
from internify.company.urls import bp as company_bp
from internify.coordinator.urls import bp as coordinator_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        JWT_SECRET_KEY="super-secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///internify.db",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
    )

    # CORS ayarlarını yapılandır
    CORS(app, supports_credentials=True)  # Tüm kaynaklardan gelen istekleri kabul et

    migrate = Migrate(app, db)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)  

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(coordinator_bp)
    return app
