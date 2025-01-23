from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = "kFvErYl_x4-aAbB3lQTO8MkWpFZPBNB1zJ5vCeT4Va"  # Replace with your secure secret key
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # Simulate returning a user object (replace this with a database lookup)
        return {"email": email, "id": 1}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
