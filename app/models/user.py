from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database.db import db
import uuid

class User(db.Model):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    avatar = Column(String)
    provider = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow())