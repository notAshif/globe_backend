from flask import Blueprint, jsonify, request
from app.utils.jwt import verify_token
import requests
import os
from datetime import datetime, timedelta

secret_bp = Blueprint("secret", __name__, url_prefix="/secret")

ADMIN_EMAILS = ["testuser1@work.com", "demo.x@twitter.com", "demo.google@gmail.com"]

def is_admin(req):
    auth_header = req.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        return False
    from app.models.user import User
    from app.database.db import db
    user = db.session.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        return False
    return user.email in ADMIN_EMAILS

@secret_bp.route("/verify", methods=["GET"])
def verify_admin():
    if not is_admin(request):
        return {"error": "ACCESS DENIED"}, 403
    return jsonify({"access": True, "clearance": "LEVEL 5 - TOP SECRET"})

@secret_bp.route("/conflicts", methods=["GET"])
def get_conflicts():
    if not is_admin(request):
        return {"error": "ACCESS DENIED"}, 403
    try:
        resp = requests.get("https://ucdpapi.pcr.uu.se/api/gedevents/24.1?pagesize=50", timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("Result", [])
            conflicts_map = {}
            for event in data:
                name = event.get("conflict_name", "Unknown Conflict")
                if name not in conflicts_map:
                    conflicts_map[name] = {
                        "id": f"CF-{event.get('conflict_new_id')}",
                        "name": name,
                        "region": event.get("region", "Global"),
                        "status": "ACTIVE",
                        "threat_level": "CRITICAL" if event.get("deaths_total", 0) > 20 else "HIGH",
                        "parties": [event.get("side_a", ""), event.get("side_b", "")],
                        "casualties_est": f"{event.get('deaths_total', 0)}+",
                        "start_date": event.get("date_start", "").split("T")[0] if event.get("date_start") else "2024",
                        "description": f"Conflict activity in {event.get('adm_1', 'the region')}.",
                        "lat": event.get("latitude"),
                        "lng": event.get("longitude")
                    }
                else:
                    try:
                        old = int(conflicts_map[name]["casualties_est"].replace("+", ""))
                        conflicts_map[name]["casualties_est"] = f"{old + event.get('deaths_total', 0)}+"
                    except: pass
            return jsonify({"conflicts": list(conflicts_map.values())[:10], "total": len(conflicts_map)})
        print(f"Conflict API Status: {resp.status_code}")
    except Exception as e:
        print(f"Conflict Error: {e}")
    return jsonify({"conflicts": [], "error": "Live feed unavailable", "total": 0})

@secret_bp.route("/cyber-threats", methods=["GET"])
def get_cyber_threats():
    if not is_admin(request):
        return {"error": "ACCESS DENIED"}, 403
    try:
        resp = requests.get("https://urlhaus-api.abuse.ch/v1/urls/recent/", timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("urls", [])
            threats = []
            for item in data[:15]:
                threats.append({
                    "id": f"CTH-{item.get('id')}",
                    "name": f"NODE_{item.get('id')}",
                    "type": item.get("threat", "Malware"),
                    "origin": "Distributed",
                    "target_sectors": item.get("tags") if item.get("tags") else ["Generic"],
                    "severity": "CRITICAL" if item.get("url_status") == "online" else "HIGH",
                    "status": item.get("url_status", "active").upper(),
                    "method": "Payload Delivery",
                    "description": f"Target: {item.get('url')[:50]}...",
                    "iocs": 1,
                    "affected_countries": 1
                })
            return jsonify({"threats": threats, "total": len(threats)})
        print(f"Cyber API Status: {resp.status_code}")
    except Exception as e:
        print(f"Cyber Error: {e}")
    return jsonify({"threats": [], "error": "Intel nodes offline", "total": 0})

@secret_bp.route("/intelligence", methods=["GET"])
def get_intelligence():
    if not is_admin(request):
        return {"error": "ACCESS DENIED"}, 403
    try:
        from config.config import config
        query = "(espionage) OR (cyber warfare) OR (intelligence agency)"
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=10&apiKey={config.NEWS_API_KEY}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            articles = resp.json().get("articles", [])
            intel = []
            for i, art in enumerate(articles):
                intel.append({
                    "id": f"INT-{i}",
                    "classification": "TOP SECRET // SI" if i < 3 else "SECRET",
                    "timestamp": art.get("publishedAt"),
                    "source": art.get("source", {}).get("name", "SIGINT").upper(),
                    "title": art.get("title"),
                    "summary": art.get("description"),
                    "priority": "FLASH" if i < 2 else "IMMEDIATE"
                })
            return jsonify({"intelligence": intel, "total": len(intel)})
    except Exception as e:
        print(f"Intel Error: {e}")
    return jsonify({"intelligence": [], "error": "Signals lost", "total": 0})
