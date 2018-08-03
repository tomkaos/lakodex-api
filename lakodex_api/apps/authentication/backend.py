from .serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'user': UserSerializer(user, context={'request': request}).data,
        'token': token
    }
