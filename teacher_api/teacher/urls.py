from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import TeacherView
from rest_framework import routers


router = routers.SimpleRouter()
router.register("teacher", TeacherView)

urlpatterns = [path("auth/", obtain_auth_token), path("", include(router.urls))]
