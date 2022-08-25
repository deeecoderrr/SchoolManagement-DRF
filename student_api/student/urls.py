from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import StudentView


router = routers.SimpleRouter()
router.register("student", StudentView)

urlpatterns = [path("auth/", obtain_auth_token), path("", include(router.urls))]
