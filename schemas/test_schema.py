def test_serializer(test) -> dict:
    return {
        'test_id': str(test['_id']),
        'test_name': test['test_name'],
        'start_time': test['start_time'],
        'end_time': test['end_time'],
        'start_date': test['start_date'],
        'end_date': test['end_date'],
        'duration': test['duration'],
        'topic_id': test['topic_id'],
    }


def test_detail_serializer(test_detail) -> dict:
    return {
        'test_id': str(test_detail['_id']),
        'test_name': test_detail['test_name'],
        'start_time': test_detail['start_time'],
        'end_time': test_detail['end_time'],
        'start_date': test_detail['start_date'],
        'end_date': test_detail['end_date'],
        'duration': test_detail['duration'],
        'questions': test_detail['questions'],
        'topic_id': test_detail['topic_id'],
    }


def tests_serializer(tests) -> list:
    return [test_serializer(test) for test in tests]
