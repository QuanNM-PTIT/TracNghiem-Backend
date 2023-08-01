from fastapi import APIRouter, Depends, status, HTTPException
from config import JWTtoken
from config.JWTtoken import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from config.hashing import Hash
from models.user_model import User
from config.database import user_collection
from schemas.user_schema import user_serializer
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post('/register')
def register(user: User):
    new_user = {
        'username': user.username,
        'email': user.email,
        'password': Hash.bcrypt(user.password),
        'role': user.role
    }
    existing_user = user_collection.find_one({'email': user.email})

    if existing_user:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            detail='Email đã được sử dụng.')

    _id = user_collection.insert_one(new_user)
    new_user = user_collection.find_one({'_id': _id.inserted_id})
    return {
        'status': status.HTTP_200_OK,
        'data': user_serializer(new_user)
    }


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends()):
    this_user = user_collection.find_one({'email': user.username})
    if not this_user or not Hash.verify(user.password, this_user['password']):
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            detail='Thông tin đăng nhập không chính xác.')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": this_user['email'], "role": this_user['role'], "user_id": str(this_user['_id'])},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/get_current_user')
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return JWTtoken.verify_token(token, credentials_exception)
