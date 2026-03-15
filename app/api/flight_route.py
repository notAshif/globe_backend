from flask import Blueprint, jsonify, request
from app.service.flight_service import get_flight

flight_db = Blueprint('flight', __name__, url_prefix="/flight")

@flight_db.route("/", methods=["GET"])
def flight():
    res = get_flight()
    return jsonify(res)