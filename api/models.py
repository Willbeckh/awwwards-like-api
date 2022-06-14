from django.db import models
from django.contrib.auth.models import User


# todo: create user profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    bio = models.TextField('user bio')
    projects = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='projects', blank=True, null=True)

    def __str__(self):
        return self.user.username


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200, default='project')
    image_file = models.ImageField(upload_to='images/', blank=True)
    description = models.TextField('project description')
    url = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # model data display representation
    def __str__(self):
        return self.name
