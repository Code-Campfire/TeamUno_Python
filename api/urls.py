
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views
from api.views import PostViewSet, Profiles, Users, test_view #Edwin Moz added Post import
from .views.auth import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", Users, "user")
## ///////////START CODE ADDED BY EDWIN MOZ ##
router.register(r"posts", PostViewSet, "post")
## ///////////END CODE ADDED BY EDWIN MOZ ##
router.register(r"profiles", Profiles, "profile") 
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('test/', views.test_view),
    path('', include(router.urls))
]
