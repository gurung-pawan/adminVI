import bcrypt
from cryptography.fernet import Fernet

def generate_new_key() -> bytes:
    fkey = Fernet.generate_key()
    return fkey

def validate_key(key: bytes) -> bool:
    try:
        Fernet(key)
    except Exception:
        return False
    return True
        

def encrypt(data: str, key: bytes) -> bytes:
    return Fernet(key).encrypt(data.encode())

def decrypt(data: str, key: bytes) -> bytes:
    return Fernet(key).decrypt(data.encode())

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def compare_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)