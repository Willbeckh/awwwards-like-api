from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User, Group
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# local imports
from api.serializers import *
from api.models import Project, Profile, Rating


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
        search_fields = ['description', 'name']
        filter_backends = (filters.SearchFilter,)
        parser_class = (FileUploadParser, MultiPartParser, JSONParser)
        permission_classes = [permissions.IsAuthenticated]
    except Project.DoesNotExist:
        HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # def post(self, request, *args, **kwargs):
    #     file_serializer = ProjectSerializer(data=request.data)

    #     if file_serializer.is_valid():
    #         file_serializer.save()
    #         return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # rating system for projectss
    @action(detail=True, methods=['POST'])
    def rate_project(self, request, pk=None):
        if 'stars' in request.data:
            try:  # get a project and check if it is rated
                project = Project.objects.get(id=pk)
                stars = request.data['stars']
                user = User.objects.get(pk=1)
                try:  # check if the user has already rated the project
                    rating = Rating.objects.get(
                        user=user.id, project=project.id)
                    rating.stars = stars
                    rating.save()
                    serializer = RatingSerializer(rating, many=False)
                    response = {'message': 'Rating updated',
                                'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                except:  # if the user has not rated the project, create a new rating/ update the rating
                    rating = Rating.objects.create(
                        user=user, project=project, stars=stars)
                    serializer = RatingSerializer(rating, many=False)
                    response = {'message': 'Rating created!',
                                'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
            # if the project does not exist, return a 404
            except Project.DoesNotExist:
                response = {'message': 'Project does not exist'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = {'message': 'Please leave a star rating'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# django app views
class HomeView(View):
    def get(self, request):
        projects = Project.objects.all()
        ctx = {
            'projects': projects
        }
        return render(request, 'index.html', ctx)