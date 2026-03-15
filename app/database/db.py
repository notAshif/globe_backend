from flask_sqlalchemy import SQLAlchemy
from config.config import config

db = SQLAlchemy()

def init_db(app):
    db_url = config.DATABASE_URL or ""
    
    db_url = db_url.strip().strip("'").strip('"')
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+pg8000://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)
        
    # pg8000 doesn't support channel_binding or sslmode, remove them
    if "channel_binding" in db_url:
        import re
        db_url = re.sub(r'[&?]channel_binding=[^&]*', '', db_url)
    if "sslmode" in db_url:
        import re
        db_url = re.sub(r'[&?]sslmode=[^&]*', '', db_url)
        
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    db.init_app(app)

def get_db():
    return db.session()