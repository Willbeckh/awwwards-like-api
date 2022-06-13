from email.headerregistry import Group
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from django.http import HttpResponse

# local imports
from api.serializers import UserSerializer, GroupSerializer, ProjectSerializer
from api.models import Project

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    endpoint that allows user to view or edit user data.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

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
        permission_classes = [permissions.IsAuthenticated]
    except Project.DoesNotExist:
        HttpResponse(status=404)
