import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from .serializers import UserSerializer


@api_view(['POST'])
@csrf_exempt
def registration(request):
    try:
        UserJson = json.loads(json.dumps(request.data))
    except Exception as e:
        context = {"data": {},
                   "Status": False,
                   "Message": e
                   }
        return Response(context)
    if UserJson:
        if User.objects.filter(Email=UserJson.get('email')).exists():
            context = {
                "Status": False,
                "Message": 'User Already Exist..!'
            }
            return Response(context)
        else:
            User(Username=UserJson.get('username'), Email=UserJson.get('email'),
                 Password=UserJson.get('password'),
                 Confirm_password=UserJson.get('confirm_password'),
                 ).save()
            context = {
                "Status": True,
                "Message": 'User register Successfully..!'
            }
            return Response(context)


@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        UserJson = json.loads(json.dumps(request.data))
    except Exception as e:
        context = {
                   "Status": False,
                   "Message": e
                   }
        return Response(data=context)
    if UserJson:
        try:
            userObject = User.objects.get(Email=UserJson.get('email'))
        except:
            context = {
                       "Status": False,
                       "Message": "Email dose not exist..!"
                       }
            return Response(data=context)
        if userObject and userObject.Password == UserJson.get('password'):

            context = {

                "Status": True,
                "Message": 'Login Successfull..!'
            }
            return Response(data=context)
        else:
            context = {
                "Status": False,
                "Message": 'Password not Matched..!'
            }
            return Response(data=context)
    else:
        context = {
            "Status": False,
            "Message": 'Email and Password cannot be empty..!'
        }
        return Response(data=context)


