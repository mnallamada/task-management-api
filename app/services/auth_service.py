from app.models.user import User
from app.utils.hashing import hash_password, verify_password
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user.
    """
    print("Debug: Authenticating user...")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"Debug: User with email {email} not found.")
        return None

    if not verify_password(password, user.hashed_password):
        print("Debug: Invalid password.")
        return None

    print(f"Debug: User {user.email} authenticated successfully.")
    return user
