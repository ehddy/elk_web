from config.default import *
from logging.config import dictConfig

# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, '.db'))
SQLALCHEMY_DATABASE_URI = 'postgresql://ehddy:4631@db:5432/flask_db' 

SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = b'S\x05\xea\xa4\x1c\xd8\x85\xe5x%\xbeQ\xaa\x15\xbc\n'
