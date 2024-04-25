from rest_framework import viewsets
from .import models
from .import serializers



class ProfileViewset(viewsets.ModelViewSet):
    queryset=models.Profile.objects.all()
    serializer_class=serializers.ProfileSerializer



class FileViewset(viewsets.ModelViewSet):
    queryset=models.File.objects.all()
    serializer_class=serializers.FileSerializer


class DataUploadViewset(viewsets.ModelViewSet):
    queryset=models.DataUpload.objects.all()
    serializer_class=serializers.DataUploadSerializer
    