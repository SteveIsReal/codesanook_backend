from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .throttle import LoginThrottle
from .serializers import UserSerializer
from django.contrib.auth.models import User


class MeView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class LoginView(TokenObtainPairView):
  throttle_classes = [LoginThrottle] 