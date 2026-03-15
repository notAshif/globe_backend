from app.database.db import db
from sqlalchemy import Column, String, DateTime

class Flight(db.Model):
    __tablename__ = "flights"
    
    flight_id = Column(String, primary_key=True)
    airline = Column(String)
    origin = Column(String)
    destination = Column(String)
    status = Column(String)
    lat = Column(String)
    lnd = Column(String)