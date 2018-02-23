
from djmodel.models import Group, User, File, File_Permission, Stars  # , Profile
from djmodel.serializers import UserSerializer, GroupSerializer  # , FileSerializer
from djmodel.serializers import FilePermissionSerializer, StarsUpVoteSerializer
from djmodel.serializers import UserRegistrationSerializer, UserSerializerLogin
from djmodel.serializers import UserSerializerUpdate, UserByGroupSerializer, TokenSerializer
from djmodel.serializers import UserByNameSerializer, UserDiskUtilizationSerializer
from djmodel.serializers import FiledownloadSerializer, FileOrderingSerializer
from djmodel.serializers import FileGetInfoSerializer
# from djmodel.serializers import StarsSerializer
# from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView  # , ListView
# from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser
from rest_framework.generics import CreateAPIView, GenericAPIView
# ListAPIView
from random import randint


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializerLogin

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogoutAPIView(APIView):

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


# users


class UserView(APIView):

    @staticmethod
    def get(request):
        """
        List users
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)


# users/{sap_id}
class UserDetail(APIView):

    @staticmethod
    def get(request, sap_id):
        """
        View individual user
        """

        user = get_object_or_404(User, pk=sap_id)
        return Response(UserSerializer(user).data)

    @staticmethod
    def patch(request, sap_id):
        """
        Update authenticated user
        """

        user = get_object_or_404(User, pk=sap_id)
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializerUpdate(user, data=request.data, context={'request': request},
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializerLogin(serializer.instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, sap_id):
        """
        Delete user
        """

        user = get_object_or_404(User, pk=sap_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserByGroupView(APIView):

    @staticmethod
    def get(request, group):
        """
        get all users belonging to group
        """
        user1 = User.objects.filter(group=group)
        # return Response(UserByGroupSerializer(users).data)
        if not user1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(UserByGroupSerializer(user1, many=True).data)


class UserByNameView(APIView):

    @staticmethod
    def get(request, name):
        """
        Get all users with same name
        """

        user1 = User.objects.filter(name=name)
        user = list(user1)
        if not user1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(UserByNameSerializer(user, many=True).data)
        # return Response()


class UserDiskUtilizationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request):
        """
        Get disk_utilization of authenticated user
        """
        users = User.objects.all()
        return Response(UserDiskUtilizationSerializer(users).data)


class FileGetAllView(APIView):
    @staticmethod
    def get(request, start_idx, end_idx, sort_by, sort_order):
        '''
        Get all files from start_idx to end_idx
        '''
        if sort_order == 'ascending':
            # if sort_by == 'size':
            #     file = File.objects.order_by('size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'recent':
                file = File.objects.order_by('time_added')[start_idx:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.order_by('no_of_stars')[start_idx:end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)
        if sort_order == 'descending':
            # if sort_by == 'size':
            #     file = File.objects.order_by('-size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'recent':
                file = File.objects.order_by('-time_added')[start_idx:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.order_by('-no_of_stars')[start_idx:end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)


class FileGetByUserView(APIView):
    @staticmethod
    def get(request, sap_id, start_idx, end_idx, sort_by, sort_order):
        '''
        Get all files of a particular user
        '''
        user = get_object_or_404(User, pk=sap_id)
        if sort_order == 'ascending':
            # if sort_by == 'size':
            #    file = File.objects.get(submitted_by=user).order_by('size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(submitted_by=user).order_by('time_added')[start_idx - 1:
                                                                                     end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(submitted_by=user).order_by('no_of_stars')[(start_idx -
                                                                                       1):end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)
        if sort_order == 'descending':
            # if sort_by == 'size':
            #    file = File.objects.get(submitted_by=user).order_by('-size')[start_idx:end_idx]
            #    return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(submitted_by=user).order_by('-time_added')[start_idx - 1:
                                                                                      end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(submitted_by=user).order_by('-no_of_stars')[(start_idx -
                                                                                        1):end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)


class FileGetByNameView(APIView):
    @staticmethod
    def get(request, file_name, start_idx, end_idx, sort_by, sort_order):
        '''
        Get a file by name
        '''
        if sort_order == 'ascending':
            # if sort_by == 'size':
            #     file = File.objects.get(name=file_name).order_by('size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(name=file_name).order_by('time_added')[start_idx:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(name=file_name).order_by('no_of_stars')[start_idx:
                                                                                    end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)
        if sort_order == 'descending':
            # if sort_by == 'size':
            #     file = File.objects.get(name=file_name).order_by('-size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(name=file_name).order_by('-time_added')[start_idx:
                                                                                   end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(name=file_name).order_by('-no_of_stars')[start_idx:
                                                                                     end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)


class FileGetInfoView(APIView):

    @staticmethod
    def get(request, file_id):
        """
        Get info of a particular file
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        try:
            File.objects.get(file_id=file_id)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(FileGetInfoSerializer(File.objects.get(file_id=file_id)).data)


class FileDownloadView(APIView):

    @staticmethod
    def get(request, file_id):
        """
        List users
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        file1 = File.objects.get(file_id=file_id)
        return Response(FiledownloadSerializer(file1).data)


class FileDeleteView(APIView):
    @staticmethod
    def delete(request, file_id):
        """
        Delete file
        """

        file = get_object_or_404(File, pk=file_id)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class File_PermissionViewSet(viewsets.ModelViewSet):
    queryset = File_Permission.objects.all()
    serializer_class = FilePermissionSerializer


class StarFileView(APIView):
    @staticmethod
    def get(request, file_id):
        '''
        Star a file
        '''
        files = get_object_or_404(File, pk=file_id)
        files.no_of_stars += 1
        files.save()
        star = Stars.objects.filter(file=files)
        star.star_id = int(str(file_id) + str(randint(0, 10000)))
        for i in star:
            star.save(['star_id'])
        print(star.star_id)
        return Response(StarsUpVoteSerializer(star, many=True).data)


class UnStarFileView(APIView):
    @staticmethod
    def get(request, file_id):
        '''
        Unstar a file
        '''
        files = get_object_or_404(File, pk=file_id)
        files.no_of_stars -= 1
        files.save()
        star = Stars.objects.filter(file=files)
        star.star_id = str(file_id) + str(randint(0, 10000))
        for i in star:
            star.save(['star_id'])
        print(star)
        return Response(StarsUpVoteSerializer(star, many=True).data)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, name, description, file_data, format=None):
        '''
        Upload file
        '''
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        extension = file_data.split(".").lower()[-1]
        print(extension)
        return Response(file_obj.file_id, status.HTTP_201_CREATED)
