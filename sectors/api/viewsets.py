from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from sectors.api import serializer
from sectors.models import sectors, userSectors, sectorsImage, branch, sectorsGroup
from django_filters.rest_framework import DjangoFilterBackend

from utils.paginator import YourPaginationLimit

class userSectorsViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.userSectorsSerializers
    queryset = userSectors.objects.all()
    
class sectorsViewset(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated, )
    queryset = sectors.objects.all()
    serializer_class = serializer.sectorsSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['name', 'is_active','sectorGroup', 'branchName']
    search_fields = ['name']
    ordering_fields = ['name']

class sectorsGroupViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = sectorsGroup.objects.all()
    serializer_class = serializer.sectorsGroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['name', 'is_active', 'branchName', 'id']
    search_fields = ['name']
    ordering_fields = ['name']

#End point para trazer as imagens em vez de o id
class sectorsHomeViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']
    queryset = sectors.objects.all()
    serializer_class = serializer.SectorImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active', 'sectorGroup']
    search_fields = ['name']
    ordering_fields = ['name']

#End point para trazer as imagens em vez de o id
class sectorsGroupHomeViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get']
    queryset = sectorsGroup.objects.all()
    serializer_class = serializer.SectorGroupImageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active', 'branchName']
    search_fields = ['name']
    ordering_fields = ['name']

class imageSectorsViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializer.imageSectorsSerializers
    queryset = sectorsImage.objects.all()
    
class branchViewset(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated, )
    serializer_class = serializer.branchSerializers
    pagination_class = YourPaginationLimit
    queryset = branch.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['address', 'number','is_active']
    search_fields = ['address','number']
    ordering_fields = ['number', 'address', 'is_active']
    