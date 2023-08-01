import random
from bson import ObjectId
from fastapi import APIRouter, Depends
from models.question_model import QuestionDetail
from routers.authentication_router import get_current_user
from config.database import question_collection, answer_collection, test_detail_collection
from schemas.question_schema import question_detail_serializer, question_detail_serializer_for_test

router = APIRouter(
    prefix='/question',
    tags=['Question']
)


@router.get('')
def get_all_question(current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    questions = question_collection.find()
    response = []

    for question in questions:
        item = {}
        item['question'] = question
        answers = list(answer_collection.find({'question_id': str(question['_id'])}))
        random.shuffle(answers)
        item['answers'] = answers
        response.append(question_detail_serializer(item))

    return {
        'status': 200,
        'data': response
    }


@router.get('/question_and_answers')
def get_all_question(current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    questions = question_collection.find()
    response = []

    for question in questions:
        item = {}
        item['question'] = question
        answers = list(answer_collection.find({'question_id': str(question['_id'])}))
        random.shuffle(answers)
        item['answers'] = answers
        response.append(question_detail_serializer_for_test(item))

    return {
        'status': 200,
        'data': response
    }


@router.get('/question_and_answers/{question_id}')
def get_all_question(question_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You do not have permission to access this page!'
        }

    question = question_collection.find_one({'_id': ObjectId(question_id)})
    response = {}
    response['question'] = question
    answers = list(answer_collection.find({'question_id': str(question['_id'])}))
    random.shuffle(answers)
    response['answers'] = answers

    return {
        'status': 200,
        'data': question_detail_serializer_for_test(response)
    }


@router.post('/add_question')
def add_question(request: QuestionDetail, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    question = {
        'question_content': request.question_content
    }

    _id = question_collection.insert_one(question)

    for item in request.answers:
        answer = {
            'question_id': str(_id.inserted_id),
            'answer_content': item.answer_content,
            'is_correct': item.is_correct
        }

        answer_collection.insert_one(answer)

    return {
        'status': 200,
        'data': 'Add question successfully!'
    }


@router.delete('/delete_question/{question_id}')
def delete_question(question_id: str, current_user=Depends(get_current_user)):
    if current_user.role != 'Admin':
        return {
            'status': 401,
            'data': 'You are not authorized to access this page.'
        }

    question_exists = question_collection.find_one({'_id': ObjectId(question_id)})

    if not question_exists:
        return {
            'status': 404,
            'data': 'Question not found!'
        }

    question_collection.delete_one({'_id': ObjectId(question_id)})
    answer_collection.delete_many({'question_id': question_id})
    test_detail_collection.delete_many({'question_id': question_id})

    return {
        'status': 200,
        'data': 'Delete question successfully!'
    }
