from django.urls import path, include

# local app imports
from . import views
from .views import HomeView, ProjectView, UserRegisterView, UserLoginView, LogoutView


app_name = 'awards'
urlpatterns = [
    # app endpoints
    path('', HomeView.as_view(), name='home'),
    path('project/<int:id>', ProjectView.as_view(), name='project'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
