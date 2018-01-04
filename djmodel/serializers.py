from rest_framework import serializers
from djmodel.models import Group, User, File, File_Permission, Stars


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('sap_id', 'name', 'password', 'bio', 'created',
                  'disk_utilization', 'group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('category', 'year', 'division', 'group_id',
                  'total_disk_available')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('size', 'time_added', 'name', 'file_id',
                  'type1', 'submitted_by',
                  'no_of_downloads', 'no_of_stars', 'file_data')


class FilePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_Permission
        fields = ('permission_id', 'shared_with', 'file')


class StarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = ('file_id', 'starred_by', 'file')
