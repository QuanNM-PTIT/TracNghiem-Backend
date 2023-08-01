def user_serializer(user) -> dict:
    return {
        'user_id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'role': user['role']
    }


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]