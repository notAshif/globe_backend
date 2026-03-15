from flask import Blueprint, jsonify, request
from app.service.news_service import fetch_global_news

news_bp = Blueprint("news", __name__, url_prefix="/news")

@news_bp.route("/", methods=["GET"])
def get_news():
    category = request.args.get("category")
    res = fetch_global_news(category=category)
    return jsonify(res)

@news_bp.route("/country/<country>", methods=["GET"])
def get_country_news(country):
    category = request.args.get("category")
    res = fetch_global_news(country=country, category=category)
    return jsonify(res)