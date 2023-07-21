from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flaskext.markdown import Markdown
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    # # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models 

    from .views import main_views, auth_views, user_views, model_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(model_views.bp)
    
    # 필터 
    # from .filter import format_datetime
    # app.jinja_env.filters['datetime'] = format_datetime

    return app
