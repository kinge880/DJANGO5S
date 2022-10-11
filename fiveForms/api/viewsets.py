from datetime import datetime
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from fiveForms.api import serializer
from fiveForms.models import fiveForm, fiveFormAsk, fiveFormResponse, fiveFormResponseImage
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginator import CustomPagination

class fiveFormViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.fiveFormSerializer
    queryset = fiveForm.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = {'title':['exact'],
                        'sectorId':['exact'],
                        'end_at':['gte', 'lte'],
                        'start_at':['gte', 'lte']}
    search_fields = ['title']
    ordering_fields = ['title']
    

class askViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.askSerializer
    queryset = fiveFormAsk.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['formId']
    

class responseViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    serializer_class = serializer.responseSerializer
    queryset = fiveFormResponse.objects.all().order_by('askId')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['formId', 'askId']

class responseImageViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.responseImageSerializer
    queryset = fiveFormResponseImage.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id']


#Viewsets para a geração do relatório

class Forms5sRelatoryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    serializer_class = serializer.fiveFormRelatorySerializer
    http_method_names = ['get']
    queryset = fiveForm.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = {'title':['exact'],
                        'sectorId':['exact'],
                        'end_at':['gte', 'lte'],
                        'start_at':['gte', 'lte']}
    search_fields = {'end_at':['gte', 'lte'],
                    'start_at':['gte', 'lte']}
    ordering_fields = ['title']
    
class Relatory5SViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination
    serializer_class = serializer.responseWithImageRelatorySerializer
    http_method_names = ['get']
    queryset = fiveFormResponse.objects.all().order_by('askId')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['formId', 'askId', 'id', 'userId']