from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    bio = models.TextField('user bio', blank=True)
    projects = models.ManyToManyField(
        'Project', related_name='projects', blank=True)

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
    url = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # model data display representation
    def __str__(self):
        return self.name

    # get number of ratings
    def all_ratings(self):
        ratings = Rating.objects.filter(project=self).count()
        return ratings

    # average ratings
    def avg_ratings(self):
        sum = 0
        ratings = Rating.objects.filter(project=self)
        for rating in ratings:
            sum += rating.stars

        if ratings.count() > 0: # prevents division by zero
            return sum/len(ratings)
        return 0

    # return all user projects
    @classmethod
    def get_all_projects(cls, user_id):
        return cls.objects.filter(pk=user_id)


RATE_CHOICES = [
    (1, '1 - Poor'),
    (2, '2 - Try Again'),
    (3, '3 - Do Better'),
    (4, '4 - Not bad'),
    (5, '5 - OK'),
    (6, '6 - Mmmh'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Classical'),
    (10, '10 - Master Piece'),
]


# rating model
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    review = models.TextField(max_length=3000, blank=True)
    stars = models.PositiveSmallIntegerField(choices=RATE_CHOICES, default=0)
    # for design
    # for perfomance
