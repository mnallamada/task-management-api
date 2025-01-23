from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_session_local
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import create_user, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import jwt

# JWT Configuration
SECRET_KEY = "kFvErYl_x4-aAbB3lQTO8MkWpFZPBNB1zJ5vCeT4Va"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_session_local)):
    """Sign up a new user."""
    return create_user(db, user)
    

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session_local),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"first_name": user.first_name, "last_name": user.last_name},
    }



@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_session_local)):
    """List all users."""
    users = db.query(User).all()
    return users
