def answer_content_serializer(answer) -> dict:
    return {
        'answer_id': str(answer['_id']),
        'answer_content': str(answer['answer_content'])
    }


def answer_serializer(answer) -> dict:
    return {
        'answer_id': str(answer['_id']),
        'answer_content': str(answer['answer_content']),
        'is_correct': answer['is_correct']
    }


def answers_content_serializer(answers) -> list:
    return [answer_content_serializer(answer) for answer in answers]


def answers_serializer(answers) -> list:
    return [answer_serializer(answer) for answer in answers]
