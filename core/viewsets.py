from rest_framework import viewsets
from .import models
from .import serializers



class UserViewset(viewsets.ModelViewSet):
    queryset=models.User.objects.all()
    serializer_class=serializers.UserSerializer

