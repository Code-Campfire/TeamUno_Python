from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api.models import *
from . import views
from views import Profiles, Users ## CODE ADDED BY EDWIN MOZ ##

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", Users, "user")
router.register(r"profiles", Profiles, "profile") ## CODE ADDED BY EDWIN MOZ ##

urlpatterns = [
    path('test/', views.test_view),
    path('', include(router.urls)) ## CODE ADDED BY EDWIN MOZ ##
]