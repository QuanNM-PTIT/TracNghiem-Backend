import json
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends
from models.test_detail_model import TestDetail
from models.test_model import AddTest
from schemas.test_schema import tests_serializer, test_detail_serializer
from config.database import test_collection, topic_detail_collection, test_detail_collection, question_collection, \
    answer_collection, attemp_collection
from routers.authentication_router import get_current_user
from models.attemp_model import Attemp
from config.redis_config import rd
from schemas.question_schema import question_detail_serializer
import random

router = APIRouter(
    prefix='/test',
    tags=['Test']
)


@router.get('')
def get_all_test(current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    tests = rd.get('tests')

    if not tests:
        tests = tests_serializer(test_collection.find())
        rd.set('tests', json.dumps(tests))
        rd.expire('tests', 30)
    else:
        tests = json.loads(tests)

    return {
        'status': 200,
        'data': tests
    }


@router.get('/{topic_id}')
def get_all_test(topic_id: str):
    topic_details = topic_detail_collection.find({"topic_id": topic_id})
    test_ids = [ObjectId(topic_detail["test_id"]) for topic_detail in topic_details]
    tests = tests_serializer(test_collection.find({"_id": {"$in": test_ids}}))

    if not tests:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    return {
        "status": 200,
        "data": tests
    }


@router.get('/detail/{test_id}')
def get_test_by_id(test_id: str, current_user=Depends(get_current_user)):
    test = test_collection.find_one({'_id': ObjectId(test_id)})

    if not test:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    start_date = datetime.strptime(test['start_date'] + ' - ' + test['start_time'], '%d/%m/%Y - %H:%M')
    end_date = datetime.strptime(test['end_date'] + ' - ' + test['end_time'], '%d/%m/%Y - %H:%M')
    current_date = datetime.now()

    if current_user.role == 'Admin' or (start_date <= current_date <= end_date):

        test_details = test_detail_collection.find({'test_id': test_id})
        questions = []

        for test_detail in test_details:
            item = {}
            item['question'] = question_collection.find_one({'_id': ObjectId(test_detail['question_id'])})
            answers = list(answer_collection.find({'question_id': test_detail['question_id']}))
            random.shuffle(answers)
            item['answers'] = answers
            questions.append(question_detail_serializer(item))

        test['questions'] = questions

        response_test = test_detail_serializer(test)

        return {
            'status': 200,
            'data': response_test
        }

    return {
        'status': 403,
        'data': 'Ngoài thời gian làm bài!'
    }


@router.post('/detail/get_attemp')
def add_attemp(attemp: Attemp, current_user=Depends(get_current_user)):
    if current_user.role == 'Admin':
        return {
            'status': 200
        }

    test = test_collection.find_one({'_id': ObjectId(attemp.test_id)})

    if not test:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    start_date = datetime.strptime(test['start_date'] + ' - ' + test['start_time'], '%d/%m/%Y - %H:%M')
    end_date = datetime.strptime(test['end_date'] + ' - ' + test['end_time'], '%d/%m/%Y - %H:%M')
    current_date = datetime.now()

    if start_date <= current_date <= end_date:

        attemp_exits = attemp_collection.find_one({'user_id': current_user.user_id, 'test_id': attemp.test_id})

        if not attemp_exits:
            start_time = datetime.strptime(attemp.start_time, '%d/%m/%Y - %H:%M:%S')
        else:
            start_time = datetime.strptime(attemp_exits['start_time'], '%d/%m/%Y - %H:%M:%S')

        test = test_collection.find_one({'_id': ObjectId(attemp.test_id)})

        time_remaining = datetime.now() - start_time

        print(time_remaining.total_seconds(), start_time)

        if time_remaining.total_seconds() > test['duration'] * 60:
            return {
                'status': 403,
                'data': 'Ngoài thời gian làm bài!'
            }

        attemp.time_remaining = test['duration'] * 60 - time_remaining.total_seconds()

        if not attemp_exits:
            attemp_collection.insert_one(attemp.dict(by_alias=True))

        return {
            'status': 200,
            'data': attemp
        }
    else:
        return {
            'status': 403,
            'data': 'Ngoài thời gian làm bài!'
        }


@router.post('/add_test')
def add_test(test: AddTest, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    _id = test_collection.insert_one(test.dict(by_alias=True))

    topic_detail = {
        'topic_id': str(test.topic_id),
        'test_id': str(_id.inserted_id)
    }

    topic_detail_collection.insert_one(topic_detail)
    test_details = [{'test_id': str(_id.inserted_id), 'question_id': item} for item in test.selected_questions]

    if test_details:
        test_detail_collection.insert_many(test_details)

    return {
        'status': 200,
        'data': 'Test added successfully!'
    }


@router.post('/add_question')
def add_question(request: TestDetail, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    test_details = [{'test_id': request.test_id, 'question_id': item} for item in request.question_ids]

    test_detail_collection.insert_many(test_details)  # bulk_write

    return {
        'status': 200,
        'data': 'Add question successfully!'
    }


@router.delete('/delete_test/{test_id}')
def delete_test(test_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    test_exists = test_collection.find_one({'_id': ObjectId(test_id)})

    if not test_exists:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    test_collection.delete_one({'_id': ObjectId(test_id)})
    test_detail_collection.delete_many({'test_id': test_id})
    topic_detail_collection.delete_one({'test_id': test_id})

    rd.delete('tests')

    return {
        'status': 200,
        'data': 'Delete test successfully!'
    }


@router.put('/update_test/{test_id}')
def update_test(test_id: str, test: AddTest, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    test_exists = test_collection.find_one({'_id': ObjectId(test_id)})

    if not test_exists:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    test_collection.update_one({'_id': ObjectId(test_id)}, {'$set': test.dict(by_alias=True)})
    topic_detail_collection.update_one({'test_id': test_id}, {'$set': {'topic_id': str(test.topic_id)}})

    test_details = [{'test_id': test_id, 'question_id': item} for item in test.selected_questions]
    test_detail_collection.delete_many({'test_id': test_id})

    if test_details:
        test_detail_collection.insert_many(test_details)

    rd.delete('tests')
    rd.delete('topics')

    return {
        'status': 200,
        'data': 'Update test successfully!'
    }


@router.get('/get_questions/{test_id}')
def get_questions(test_id: str, current_user=Depends(get_current_user)):
    questions = []
    test_details = test_detail_collection.find({'test_id': test_id})

    if not test_details:
        return {
            'status': 404,
            'data': 'Test not found!'
        }

    for test_detail in test_details:
        item = {}
        item['question'] = question_collection.find_one({'_id': ObjectId(test_detail['question_id'])})
        answers = list(answer_collection.find({'question_id': test_detail['question_id']}))
        random.shuffle(answers)
        item['answers'] = answers
        questions.append(question_detail_serializer(item))

    return {
        'status': 200,
        'data': questions
    }


@router.get('/get_question_ids/{test_id}')
def get_question_ids(test_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    test_details = test_detail_collection.find({'test_id': test_id})
    question_ids = [test_detail['question_id'] for test_detail in test_details]

    return {
        'status': 200,
        'data': question_ids
    }