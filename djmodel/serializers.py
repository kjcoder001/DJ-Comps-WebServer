from rest_framework import serializers
from djmodel.models import Group, User, File, File_Permission, Stars

# from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):

    # profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('sap_id', 'name', 'bio', 'created',
                  'disk_utilization', 'group')


'''
    @staticmethod
    def get_profile(user):
        """
        Get or create profile
        """

        profile, created = Profile.objects.get_or_create(user=user)
        return ProfileSerializer(profile, read_only=True).data
'''


'''
class UserSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('sap_id', 'name', 'bio', 'created',
                  'disk_utilization', 'group', 'profile', 'password')

    @staticmethod
    def validate_password(password):
        """
        Validate password
        """

        validate_password(password)
        return password
'''


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('sap_id', 'name', 'bio', 'created',
                  'disk_utilization', 'group', 'profile', 'password', 'confirm_password')

    def create(self, validated_data):
        del validated_data["confirm_password"]
        return super(UserRegistrationSerializer, self).create(validated_data)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return attrs


'''
class UserSerializerLogin(UserSerializer):
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user):
        """
        Get or create token
        """

        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        model = User
        fields = ('sap_id', 'name', 'bio', 'created',
                  'disk_utilization', 'group', 'profile', 'token')
'''


class UserSerializerLogin(serializers.Serializer):

    class Meta:
        model = User

    default_error_messages = {
        'inactive_account': _('User account is disabled.'),
        'invalid_credentials': _('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserSerializerLogin, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("sap_id"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token",)


class UserSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('sap_id')


class UserByGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'sap_id')


class UserByNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'sap_id', 'group')


class UserDiskUtilizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('disk_utilization')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('category', 'year', 'division', 'group_id',
                  'total_disk_available')


class FileGetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('time_added', 'name', 'file_id',
                  'type1', 'submitted_by',
                  'no_of_downloads', 'no_of_stars', 'description')


class FileOrderingSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'file_id', 'type1')


"""

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('size', 'time_added', 'name', 'file_id',
                  'type1', 'submitted_by',

                  'no_of_downloads', 'no_of_stars', 'file_data'
                  'description')
"""


class FiledownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_data',)


class FilePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_Permission
        fields = ('permission_id', 'shared_with', 'file')


'''
class StarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = ('star_id', 'starred_by', 'file')
'''


class StarsUpVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stars
        fields = ('star_id', )


'''class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
'''
