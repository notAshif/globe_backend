from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database.db import db
import uuid

class Post(db.Model):
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    content = Column(String)
    post_to_x = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow)