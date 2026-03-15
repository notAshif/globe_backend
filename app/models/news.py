from sqlalchemy import Column, String, DateTime
from app.database.db import db
import uuid
from datetime import datetime

class News(db.Model):
    __tablename__ = "news"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    country = Column(String)
    category = Column(String)
    source = Column(String)
    url = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow())