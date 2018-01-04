from djmodel.models import Group, User, File, File_Permission, Stars
from djmodel.serializers import UserSerializer, GroupSerializer, FileSerializer
from djmodel.serializers import FilePermissionSerializer, StarsSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class File_PermissionViewSet(viewsets.ModelViewSet):
    queryset = File_Permission.objects.all()
    serializer_class = FilePermissionSerializer


class StarsViewSet(viewsets.ModelViewSet):
    queryset = Stars.objects.all()
    serializer_class = StarsSerializer
