from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    bio = models.TextField('user bio', blank=True)
    projects = models.ManyToManyField('Project', related_name='projects', blank=True)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def update_profile(self):
        self.update()

    def delete_profile(self):
        self.delete()


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

    # return all user projects
    @classmethod
    def get_all_projects(cls, user_id):
        return cls.objects.filter(pk=user_id)
    


# rating model
# class Rating(models.Model):
#     # add foreign key to user
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # add foreign key to project
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)

    # create rating field for design, usability, and content
