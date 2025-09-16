from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError
from ..database import db
from ..models.user import UserCreate, TokenResponse
from .utils import get_password_hash, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=201)
async def signup(user: UserCreate):
    """Create a new user account"""
    hashed = get_password_hash(user.password)
    try:
        await db.users.insert_one({
            "username": user.username, 
            "hashed_password": hashed
        })
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Username already exists")
    return {"message": "user created"}


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password"
        )
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"access_token": None, "token_type": None, "message": "Logged out successfully"}
