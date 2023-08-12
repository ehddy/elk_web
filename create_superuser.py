from monitoring.models import User
from werkzeug.security import generate_password_hash
from monitoring import db, create_app

app = create_app()  # 또는 애플리케이션을 생성하는 다른 방법을 사용하세요

with app.app_context():
    if not User.query.filter_by(username='planty').first():
        password = generate_password_hash("planty020117")
        q = User(username='planty', password=password)
        db.session.add(q)
        db.session.commit()
