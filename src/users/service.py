import bcrypt


def hash_password(password: str) -> str:
    password_hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password_hash_bytes.decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
