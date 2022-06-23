from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    bio = models.TextField('user bio', blank=True)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def update_profile(self):
        self.update()

    def delete_profile(self):
        self.delete()
        
    def create_profile(sender, **kwargs):
        user = kwargs['instance']
        if kwargs['created']:
            user_profile = Profile(user=user)
            user_profile.save()
    post_save.connect(create_profile, sender=User)