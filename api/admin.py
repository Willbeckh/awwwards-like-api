from django.contrib import admin
from django.contrib.auth.models import User

# local app imports
from api.models import Project, Profile


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Author', {'fields': ['author']}),
        ('Description', {'fields': ['description']}),
        ('Url', {'fields': ['url']}),
    ]


admin.site.register(Project, ProjectAdmin)


class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('bio', {'fields': ['bio']}),
        ('Picture', {'fields': ['profile_pic']}),
    ]
    
admin.site.register(Profile, ProfileAdmin)