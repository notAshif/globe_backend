import os
from dotenv import load_dotenv

load_dotenv()

class config:
    
    APP_NAME="Global Dashboard"
    
    DEBUG = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY", "global-dashboard-secret")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")

    X_CLIENT_ID=os.getenv("X_CLIENT_ID")
    X_CLIENT_SECRET=os.getenv("X_CLIENT_SECRET")
    X_REDIRECT_URI=os.getenv("X_REDIRECT_URI")

    NEWS_API_KEY=os.getenv("NEWS_API_KEY")
    FLIGHT_API_KEY=os.getenv("FLIGHT_API_KEY")
    
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    ALLOWED_ORIGIN = {
        FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5000"
    }