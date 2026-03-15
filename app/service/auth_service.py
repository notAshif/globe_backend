from app.utils.jwt import create_new_access_token
from app.database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

def sign_up(name, email, password):
    exist_user = db.session.query(User).filter(User.email == email).first()
    
    if exist_user:
        return { "ERROR": "user already exist!!" }
    
    hash_passwd = generate_password_hash(password)
    
    new_user = User(
        name = name,
        email = email,
        password = hash_passwd
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    token = create_new_access_token({
        "user_id": new_user.id,
        "email": new_user.email 
    })
    
    print(f"Token is created for new user!!")
    
    return {
        "message": "User created successful",
        "access_token": token
    }
    
def login_user(email, password):
    user = db.session.query(User).filter(User.email == email).first()
    
    if not user:
        return { "Error": "User not found" }
    
    if not check_password_hash(user.password, password):
        return { "error": "Invalid Password" }
    
    token = create_new_access_token({
        "user_id": user.id,
        "email": user.email  
    })
    
    return {
        "access_token": token,
        "user": {
            "_id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar
        }
    }
    
def oauth_login(email, name, provider, avatar):
    user = db.session.query(User).filter(User.email == email).first()
    
    if not user:

        user = User(
            name=name,
            email=email,
            provider=provider,
            avatar=avatar,
            password="oauth_user_no_pass"
        )
        db.session.add(user)
        db.session.commit()
    else:

        user.avatar = avatar
        db.session.commit()
        
    token = create_new_access_token({
        "user_id": user.id,
        "email": user.email  
    })
    
    return {
        "access_token": token,
        "user": {
            "_id": user.id,
            "email": user.email,
            "name": user.name,
            "avatar": user.avatar
        }
    }