from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import get_auth_data
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_in: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_in)
    to_encode.setdefault('exp', expire)
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encoded_jwt