from django.contrib import admin

# local app imports
from api.models import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Author', {'fields': ['author']}),
        ('Image', {'fields': ['image_file']}),
        ('Description', {'fields': ['description']}),
        ('Url', {'fields': ['url']}),
    ]


admin.site.register(Project, ProjectAdmin)


