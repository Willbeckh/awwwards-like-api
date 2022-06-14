from email.headerregistry import Group
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, filters, generics
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

# local imports
from api.serializers import MyTokenObtainSerializer, UserSerializer, GroupSerializer, ProjectSerializer, RegisterSerializer
from api.models import Project


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny, )
    serializer_class = MyTokenObtainSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows user to view or edit user data.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# register view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited 
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing user projects
    """
    try:
        queryset = Project.objects.all().order_by('-created_at')
        serializer_class = ProjectSerializer
        search_fields = ['description', ]
        filter_backends = (filters.SearchFilter,)
        permission_classes = [permissions.IsAuthenticated]
    except Project.DoesNotExist:
        HttpResponse(status=404)
