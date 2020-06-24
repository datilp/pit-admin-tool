from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class TestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"name": "igor",
                         "surname": "sola",
                         "pet": "Copito"})


class TestAPIView2(APIView):
    def get(self, request, *args, **kwargs):
        print("REMOTE_HOST:", request.META['REMOTE_ADDR'])
        print("HTTP_HOST:", request.META['HTTP_HOST'])
        return Response({"name": "igor",
                         "surname": "sola",
                         "pet": "Copi"})

