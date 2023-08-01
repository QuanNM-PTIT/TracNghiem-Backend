def attemp_serializer(attemp):
    return {
        'test_id': str(attemp['test_id']),
        'user_id': str(attemp['user_id']),
        'answers': attemp['answers'],
        'score': attemp['score'],
        'start_time': attemp['start_time'],
        'time_remaining': attemp['time_remaining']
    }


def attemps_serializer(attemps):
    return [attemp_serializer(attemp) for attemp in attemps]
