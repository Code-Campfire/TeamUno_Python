from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse

def test_view(request):
    return HttpResponse("This is a test view")

@api_view(['GET'])
def hello_world(request):
    print("Hello endpoint was hit!")
    return Response({"message": "Hello from CodeFire API!"})
