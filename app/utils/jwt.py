from datetime import datetime, timedelta
import jwt
from config.config import config

SECRET_KEY = config.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"

def create_new_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"TOKEN GENERATE:: {encode_jwt}")
    return encode_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"VERIFYING TOKEN:: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidAlgorithmError:
        return None