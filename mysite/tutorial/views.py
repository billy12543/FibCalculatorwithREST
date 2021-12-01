from django.http import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import json
import grpc
import paho.mqtt.publish as publish
from . import fib_pb2_grpc
from . import fib_pb2
# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)
    def post(self,request):
        j = json.loads(request.body.decode())
        j.setdefault("order",10)
        j.setdefault("clear","false")
        if j["clear"] != "false":
            print("clear history")
            publish.single(topic="C",payload='r')
            return Response(data={ 'history': "cleared" }, status=200)
        else:
            with grpc.insecure_channel("localhost:8080") as channel:
                stub = fib_pb2_grpc.FibCalculatorStub(channel)
                request = fib_pb2.FibRequest()
                request.order = int(j["order"])
                response = stub.Compute(request)
                r = str(response)
                publish.single(topic="N",payload=j["order"])
            print("order",j["order"])
            return Response(data={ 'response': f'{r[7:-1]}' }, status=200)

class LogView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        with grpc.insecure_channel("localhost:8080") as channel:
            stub = fib_pb2_grpc.FibHistoryStub(channel)
            request = fib_pb2.FibRequest()
            request.order = 1
            response = stub.Compute(request)
            r = str(response.history)
        return Response(data={ 'history': f'{r}' }, status=200)