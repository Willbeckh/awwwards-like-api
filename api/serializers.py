import base64
from re import I
import string
from rest_framework.response import Response
from rest_framework import serializers, generics
from django.contrib.auth.models import User, Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_extra_fields.fields import Base64ImageField, HybridImageField
from django.core.files.base import ContentFile

# local imports
from api.models import Project, Profile, Rating


# !Image base64 serializer
class Base64ImageField(serializers.ImageField):
    """A drf field for serializing image-uploads through post raw-data.
    """

    def from_native(self, data):
        """
        Decode the base64-encoded data and return the decoded data.
        """
        # if isinstance
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image data == decode
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)


# token serializer
class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainSerializer, cls).get_token(user)

        # custom claims
        token['username'] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    """jsonify user profile data"""
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio']


class UserSerializer(serializers.ModelSerializer):
    all_projects = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField('get_bio')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio',
                  'url', 'projects', 'all_projects']

    def get_projects(self, obj):
        projects = Project.objects.filter(author=obj.id).count()
        return projects

    def get_all_projects(self, obj, ):
        """Gets all user projects"""

        projects = Project.objects.filter(author=obj.id)
        serializer = ProjectSerializer(projects, many=True)
        return {"all_projects": serializer.data}

    def get_bio(self, obj):
        """get the user bio from profile model"""
        bio = Profile.objects.filter(user=obj.id)
        serializer = ProfileSerializer(bio)
        return serializer.data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# projects object repr serializer
class ProjectSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image_file = Base64ImageField()

    class Meta:
        model = Project
        fields = ['id', 'author', 'name',
                  'description', 'url', 'image_file', 'image_url', 'created_at', 'all_ratings', 'avg_ratings']

    def get_image_url(self, obj):
        return obj.image_file.url


# create registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'project', 'stars']
