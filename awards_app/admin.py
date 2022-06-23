from django.contrib import admin
# from django.contrib.auth.models import User
from awards_app.models import Profile

# admin.site.register(User)

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('bio', {'fields': ['bio']}),
        ('Picture', {'fields': ['profile_pic']}),
        ('Projects', {'fields': ['projects']}),
    ]


admin.site.register(Profile, ProfileAdmin)