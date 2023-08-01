from schemas.answer_schema import answers_content_serializer, answers_serializer


def question_serializer(question) -> dict:
    return {
        "question_content": question['question_content'],
    }


def question_detail_serializer(question_detail) -> dict:
    return {
        "question_id": str(question_detail['question']['_id']),
        "question_content": question_detail['question']['question_content'],
        "answers": answers_content_serializer(question_detail['answers'])
    }


def question_detail_serializer_for_test(question_detail) -> dict:
    return {
        "question_id": str(question_detail['question']['_id']),
        "question_content": question_detail['question']['question_content'],
        "answers": answers_serializer(question_detail['answers'])
    }


def questions_serializer(questions) -> list:
    return [question_serializer(question) for question in questions]
