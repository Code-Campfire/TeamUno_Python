from django.urls import path, include
from .views.auth import AuthViewSet
from rest_framework import routers
from api.views import PostViewSet, Profiles, Users, test_view #Edwin Moz added Post import

router = routers.DefaultRouter(trailing_slash=False)

router.register(r"users", Users, "user")
## ///////////START CODE ADDED BY EDWIN MOZ ##
router.register(r"posts", PostViewSet, "post")
## ///////////END CODE ADDED BY EDWIN MOZ ##
router.register(r"profiles", Profiles, "profile")
router.register(r'auth', AuthViewSet, basename='auth') 

urlpatterns = [
    path('test/', test_view),
    path('', include(router.urls)) 
]
