from django.http import JsonResponse
from rest_framework.request import Request


def ping(request: Request) -> JsonResponse:
    data = {"ping": "pong!"}
    return JsonResponse(data)
