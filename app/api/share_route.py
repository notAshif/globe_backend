from flask import Blueprint, jsonify, request
from app.service.x_service import post_to_x
from app.models.post import Post
from app.database.db import db
import os

share_bp = Blueprint("share", __name__, url_prefix="/share")

@share_bp.route("/", methods=["GET"])
def get_posts():
    from app.models.user import User
    posts_with_users = db.session.query(Post, User).outerjoin(User, Post.user_id == User.id).order_by(Post.create_at.desc()).limit(20).all()
    results = []
    for p, u in posts_with_users:
        results.append({
            "id": p.id,
            "content": p.content,
            "post_to_x": p.post_to_x,
            "user_id": p.user_id,
            "author_name": u.name if u else "Anonymous",
            "author_avatar": u.avatar if u else None,
            "author_provider": u.provider if u else None,
            "create_at": (p.create_at.isoformat() + "Z") if p.create_at else None
        })
    return jsonify(results)

@share_bp.route("/", methods=["POST"])
def create_post():
    from app.utils.jwt import verify_token
    
    auth_header = request.headers.get("Authorization")
    user_id = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload and "user_id" in payload:
            user_id = payload["user_id"]
            
    data = request.json
    content = data.get("content")
    post_to_x_flag = data.get("post_to_x", False)
    
    if not content:
        return { "error": "Content is required!!" }, 400
    

    new_post = Post(content=content, post_to_x=post_to_x_flag, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    
    res = None
    if post_to_x_flag:
        try:
            res = post_to_x(
                content,
                api_key=os.getenv("X_API_KEY"),
                api_secret=os.getenv("X_API_SECRET"),
                access_token=os.getenv("X_ACCESS_TOKEN"),
                access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
            )
            print("X API Response:", res)
        except Exception as e:
            print("Failed to post to X:", e)
            
    return jsonify({
        "message": "Post shared successful",
        "response": res
    })

@share_bp.route("/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    from app.utils.jwt import verify_token
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return { "error": "Unauthorized" }, 401
        
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    if not payload or "user_id" not in payload:
        return { "error": "Unauthorized" }, 401
        
    user_id = payload["user_id"]
    post = db.session.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        return { "error": "Post not found" }, 404
        
    if post.user_id != user_id:
        return { "error": "You can only delete your own posts" }, 403
        
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({ "message": "Post deleted successfully" })

