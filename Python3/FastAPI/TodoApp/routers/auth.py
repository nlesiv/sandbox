from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from ..database import SessionLocal
from ..models import Users
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

# openssl rand -hex 32
SECRET_KEY = "27a65b5ea6db622fe6b6644a2362989a1454253bd4379312a611868a0b50c098"
ALGORITHM = "HS256"

router = APIRouter(
   
   
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        "sub": username,
        "id": user_id,
        "role": role,
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"username": username, "id": user_id, "role": user_role}


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    email: str = Field(..., min_length=5)
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    role: str = Field(..., min_length=3)
    # is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency,  create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        is_active=True
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
def login_user(db:db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))

    return {'access_token': token, 'token_type': 'bearer'}
    
