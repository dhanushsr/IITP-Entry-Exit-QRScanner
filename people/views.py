from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser  
from django.contrib.auth.models import User, Group
from people.models import People
from rest_framework import viewsets
from people.serializers import UserSerializer, GroupSerializer, PeopleSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



class PeopleList(APIView):

    parser_classes = (MultiPartParser, JSONParser)
    
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        peoples = People.objects.all()
        serializer = PeopleSerializer(peoples, many=True)
        return Response(serializer.data)
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleDetail(APIView):
    """
    Retrieve, update or delete a code peoples.
    """
    parser_classes = (MultiPartParser, JSONParser)
    
    @csrf_exempt
    def get_object(self, pk):
        try:
            return People.objects.get(pk=pk)
        except People.DoesNotExist:
            raise Http404
    
    @csrf_exempt
    def get(self, request, pk, format=None):
        people = self.get_object(pk)
        serializer = PeopleSerializer(people)
        return Response(serializer.data)
    
    @csrf_exempt
    def put(self, request, pk, format=None):
        people = self.get_object(pk)
        serializer = PeopleSerializer(people, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @csrf_exempt
    def delete(self, request, pk, format=None):
        people = self.get_object(pk)
        people.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)