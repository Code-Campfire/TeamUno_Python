
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views
from api.views import Profiles, Users, test_view

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", Users, "user")
router.register(r"profiles", Profiles, "profile") 

urlpatterns = [
    path('test/', test_view),
    path('', include(router.urls)) 
]