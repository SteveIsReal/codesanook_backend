from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
  groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
  class Meta:
    model = User
    fields = ["id", "username", "first_name", "last_name", "email", "groups"]

  