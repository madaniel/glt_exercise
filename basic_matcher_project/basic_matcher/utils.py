from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status


def exception_handler(func):
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
        except ObjectDoesNotExist:
            return Response({"Error": "Unknown request id"}, status=status.HTTP_400_BAD_REQUEST)
        return result

    return wrapper

