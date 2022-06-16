from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_swagger.views import get_swagger_view

# local app imports
from . import views
from .views import MyObtainTokenPairView, RegisterView, RatingViewSet


# schema_view = get_swagger_view(title='Awards API')

# setting up api routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'ratings', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
