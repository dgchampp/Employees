from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from ..database import db
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user(username: str):
    """Get user from database by username"""
    return await db.users.find_one({"username": username})


async def authenticate_user(username: str, password: str):
    """Authenticate user with username and password"""
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
