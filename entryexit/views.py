from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser  
from django.contrib.auth.models import User, Group
from entryexit.models import EntryExit, Building
from people.models import People
from rest_framework import viewsets
from entryexit.serializers import EntryExitSerializer, BuildingSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import permissions


# @csrf_exempt
# @api_view(["GET"])
class EntriesList(APIView):

    parser_classes = (MultiPartParser, JSONParser)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        entries = EntryExit.objects.all()
        serializer = EntryExitSerializer(entries, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = EntryExitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntriesDetail(APIView):
    """
    Retrieve, update or delete a code peoples.
    """
    parser_classes = (MultiPartParser, JSONParser)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    @csrf_exempt
    def get_object(self, pk):
        try:
            return EntryExit.objects.get(pk=pk)
        except EntryExit.DoesNotExist:
            raise Http404
    @csrf_exempt
    def get(self, request, pk, format=None):
        people = self.get_object(pk)
        serializer = EntryExitSerializer(people)
        return Response(serializer.data)
    @csrf_exempt
    def put(self, request, pk, format=None):
        people = self.get_object(pk)
        serializer = EntryExitSerializer(people, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = EntryExit.objects.all()
    serializer_class = EntryExitSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer