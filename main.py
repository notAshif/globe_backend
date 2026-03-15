from flask import Flask
import os
from flask_cors import CORS
from app.api.auth_route import auth_bp
from app.api.flight_route import flight_db
from app.api.news_route import news_bp
from app.api.share_route import share_bp
from app.api.secret_route import secret_bp
from app.database.db import db, init_db
from flask_migrate import Migrate
import app.models.user
import app.models.post

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "global-dashboard-secret")
init_db(app)

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(flight_db)
app.register_blueprint(news_bp)
app.register_blueprint(share_bp)
app.register_blueprint(secret_bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)