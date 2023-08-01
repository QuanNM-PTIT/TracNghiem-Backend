from bson import ObjectId
from fastapi import APIRouter, Depends
from starlette import status
from config.database import user_collection
from routers.authentication_router import get_current_user
from schemas.user_schema import users_serializer, user_serializer

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('')
async def get_users(current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Bạn không có quyền truy cập.'
        }
    return {
        'status': 200,
        'message': users_serializer(user_collection.find())
    }


@router.get('/{user_id}')
async def get_user_by_id(user_id: str):
    user = user_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return {
            'status': 200,
            'message': user_serializer(user)
        }
    return {
        'status': 404,
        'message': 'User not found!'
    }


@router.delete('/{user_id}')
async def delete_user_by_id(user_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Bạn không có quyền truy cập.'
        }
    user_collection.delete_one({'_id': ObjectId(user_id)})
    return {
        'status': 200,
        'message': 'User deleted successfully!'
    }
