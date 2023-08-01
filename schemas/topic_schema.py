def topic_serializer(topic) -> dict:
    return {
        'topic_id': str(topic['_id']),
        'topic_name': topic['topic_name'],
        'topic_image': topic['topic_image']
    }


def topics_serializer(topics) -> list:
    return [topic_serializer(topic) for topic in topics]
