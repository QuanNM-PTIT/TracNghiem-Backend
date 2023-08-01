import io
import json
from bson import ObjectId
from starlette.responses import StreamingResponse
from config.minio_config import minio_client
from config.redis_config import rd
from fastapi import APIRouter, Depends, UploadFile, Form
from schemas.topic_schema import topics_serializer, topic_serializer
from config.database import topic_collection, topic_detail_collection
from routers.authentication_router import get_current_user

router = APIRouter(
    prefix='/topic',
    tags=['Topic']
)


@router.get('')
def get_all_topic():
    topics = rd.get('topics')

    if not topics:
        topics = topics_serializer(topic_collection.find())

        for topic in topics:
            topic['num_of_test'] = topic_detail_collection.count_documents({'topic_id': topic['topic_id']})

        rd.set('topics', json.dumps(topics))
        rd.expire('topics', 30)
    else:
        topics = json.loads(topics)

    return {
        'status': 200,
        'data': topics
    }


@router.get('/{topic_id}')
def get_topic_by_id(topic_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    topic = topic_collection.find_one({'_id': ObjectId(topic_id)})

    if topic:
        return {
            'status': 200,
            'data': topic_serializer(topic)
        }
    return {
        'status': 404,
        'data': 'Topic not found!'
    }


@router.post("/add_topic")
async def add_topic(topic_name: str = Form(...), cover: UploadFile = Form(...), current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    try:
        file_content = await cover.read()

        topic_id = str(ObjectId())

        minio_client.put_object("img", topic_id, io.BytesIO(file_content), len(file_content), cover.content_type)

        file_url = f"/img/{topic_id}"

        new_topic = {
            '_id': ObjectId(topic_id),
            'topic_name': topic_name,
            'topic_image': file_url
        }

        topic_collection.insert_one(new_topic)

        rd.delete('topics')

        return {"status": 200, "data": "Topic added successfully!"}

    except Exception as err:
        return {"status": 500, "error": str(err)}


@router.put('/{topic_id}')
async def update_topic_by_id(topic_id: str, topic_name: str = Form(...), cover: UploadFile = Form(...),
                             current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    topic = topic_collection.find_one({'_id': ObjectId(topic_id)})

    if not topic:
        return {
            'status': 404,
            'data': 'Topic not found!'
        }

    rd.delete('topics')

    file_content = await cover.read()

    async def process_upload_and_update():
        try:
            minio_client.put_object("img", topic_id, io.BytesIO(file_content), len(file_content), cover.content_type)

            file_url = f"/img/{topic_id}"

            topic_collection.update_one(
                {
                    '_id': ObjectId(topic_id)
                },
                {
                    '$set':
                        {
                            'topic_name': topic_name,
                            'topic_image': file_url
                        }
                })

            return {
                "status": 200,
                "data": "Topic updated successfully!"
            }
        except Exception as err:
            return {"status": 500, "error": str(err)}

    result = await process_upload_and_update()

    return result


@router.delete('/{topic_id}')
async def delete_topic_by_id(topic_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    topic = topic_collection.find_one({'_id': ObjectId(topic_id)})

    if not topic:
        return {
            'status': 404,
            'data': 'Topic not found!'
        }

    topic_collection.delete_one({'_id': ObjectId(topic_id)})

    minio_client.remove_object(object_name=f"{topic_id}", bucket_name="img")

    rd.delete('topics')

    return {
        'status': 200,
        'data': 'Topic deleted successfully!'
    }


@router.get('/get_cover/{topic_id}')
async def get_topic_image(topic_id: str):
    try:
        topic = topic_collection.find_one({'_id': ObjectId(topic_id)})

        if not topic:
            return {
                'status': 404,
                'data': 'Topic not found!'
            }

        response = minio_client.get_object(bucket_name='img', object_name=topic_id)

        image_data = response.read()

        content_type = response.headers['Content-Type']

        return StreamingResponse(io.BytesIO(image_data), media_type=content_type)

    except Exception as err:
        return {
            'status': 500,
            'error': str(err)
        }
