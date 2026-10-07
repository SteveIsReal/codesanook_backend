from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.urls import path
from .views import *

urlpatterns = [
  path("me/", MeView.as_view()),
  path("token/", TokenObtainPairView.as_view()),
  path("token/refresh/", TokenRefreshView.as_view())
]