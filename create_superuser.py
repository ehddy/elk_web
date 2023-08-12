from monitoring.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from monitoring import db
password = generate_password_hash("planty020117")

q = User(username='planty', password=password)
db.session.add(q)
db.session.commit()