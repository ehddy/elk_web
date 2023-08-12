from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from monitoring.models import User  # 유저 모델을 가져와야 함
        # 체크하여 유저가 이미 존재하지 않으면 추가
        if not User.query.filter_by(username='planty').first():
            password = generate_password_hash("planty020117")
            q = User(username='planty', password=password)
            db.session.add(q)
            db.session.commit()

    from . import models

    from .views import main_views, auth_views, user_views, model_views, manage_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(model_views.bp)
    app.register_blueprint(manage_views.bp)
    
    # 필터 
    # from .filter import format_datetime
    # app.jinja_env.filters['datetime'] = format_datetime

    return app