from datetime import timedelta

SQLALCHEMY_DATABASE_URI="sqlite:///../database_temp.sqlite"
SECRET_KEY="changeme"
SQLALCHEMY_TRACK_MODIFICATIONS=False
SESSION_PERMANENT_LIFETIME=timedelta(days=30)
TEMPLATES_FOLDER="templates"
STATIC_FOLDER="static"
