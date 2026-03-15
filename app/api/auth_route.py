from flask import Blueprint, jsonify, request, redirect, session
from app.service.auth_service import login_user, sign_up, oauth_login
from config.config import config
import requests as http_requests

import os
import hashlib
import base64
import secrets

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

oauth_store = {}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    
    email = data.get("email")
    password = data.get("password")    
    res = login_user(email, password)
    return jsonify(res)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    
    name=data.get("name")
    email=data.get("email")
    password=data.get("password")
    
    res = sign_up(name, email, password)
    
    return jsonify(res)

@auth_bp.route("/oauth", methods=["POST"])
def oauth():
    data = request.json
    
    email = data.get("email")
    name = data.get("name")
    provider = data.get("provider")
    avatar = data.get("avatar")
    
    if not email or not name:
        return {"error": "Missing oauth data"}, 400
        
    res = oauth_login(email, name, provider, avatar)
    return jsonify(res)


@auth_bp.route("/google/verify", methods=["POST"])
def google_verify():
    data = request.json
    credential = data.get("credential")
    if not credential:
        return {"error": "Missing credential"}, 400
    

    resp = http_requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}")
    if resp.status_code != 200:
        return {"error": "Invalid Google token"}, 401
    
    payload = resp.json()
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    

    if payload.get("aud") != google_client_id:
        return {"error": "Token audience mismatch"}, 401
    
    email = payload.get("email")
    name = payload.get("name", payload.get("email", "Google User"))
    avatar = payload.get("picture", "")
    
    res = oauth_login(email, name, "google", avatar)
    return jsonify(res)


@auth_bp.route("/x/authorize")
def x_authorize():
    client_id = os.getenv("X_CLIENT_ID")
    redirect_uri = os.getenv("X_REDIRECT_URI", "http://127.0.0.1:5000/auth/x/callback")
    

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()
    

    state = secrets.token_urlsafe(32)
    oauth_store[state] = {
        "code_verifier": code_verifier
    }
    
    auth_url = (
        f"https://twitter.com/i/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=tweet.read%20users.read%20offline.access"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    
    return redirect(auth_url)

@auth_bp.route("/x/callback")
def x_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    
    if not code:
        return redirect(f"{config.FRONTEND_URL}/login?error=x_auth_failed")

    

    stored = oauth_store.pop(state, None)
    if not stored:
        return redirect(f"{config.FRONTEND_URL}/login?error=x_state_mismatch")

    
    client_id = os.getenv("X_CLIENT_ID")
    client_secret = os.getenv("X_CLIENT_SECRET")
    redirect_uri = os.getenv("X_REDIRECT_URI", "http://127.0.0.1:5000/auth/x/callback")
    code_verifier = stored["code_verifier"]
    

    token_resp = http_requests.post(
        "https://api.twitter.com/2/oauth2/token",
        data={
            "code": code,
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        },
        auth=(client_id, client_secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if token_resp.status_code != 200:
        print(f"X token error: {token_resp.text}")
        return redirect(f"{config.FRONTEND_URL}/login?error=x_token_failed")

    
    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    

    user_resp = http_requests.get(
        "https://api.twitter.com/2/users/me?user.fields=profile_image_url,name,username",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if user_resp.status_code != 200:
        print(f"X user info error: {user_resp.text}")
        return redirect(f"{config.FRONTEND_URL}/login?error=x_user_failed")

    
    x_user = user_resp.json().get("data", {})
    
    email = f"{x_user.get('username', 'unknown')}@x.com"
    name = x_user.get("name", x_user.get("username", "X User"))
    avatar = x_user.get("profile_image_url", "")
    
    res = oauth_login(email, name, "x", avatar)
    

    import urllib.parse
    user_json = urllib.parse.quote(str({
        "_id": res["user"]["_id"],
        "email": res["user"]["email"],
        "name": res["user"]["name"],
        "avatar": res["user"]["avatar"]
    }))
    
    return redirect(
        f"{config.FRONTEND_URL}/login?token={res['access_token']}&user={user_json}"
    )