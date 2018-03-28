
from djmodel.models import Group, User, File, File_Permission, Stars,Notification  # , Profile
from djmodel.serializers import UserSerializer, GroupSerializer  # , FileSerializer
from djmodel.serializers import FilePermissionSerializer, StarsUpVoteSerializer
from djmodel.serializers import UserRegistrationSerializer, UserSerializerLogin,NotificationSerializer
# from djmodel.serializers import UserSerializerUpdate, UserByGroupSerializer, TokenSerializer
from djmodel.serializers import UserByGroupSerializer

from djmodel.serializers import UserByNameSerializer, UserDiskUtilizationSerializer
from djmodel.serializers import FiledownloadSerializer, FileOrderingSerializer
from djmodel.serializers import FileGetInfoSerializer, FileSerializer, NouseSerializer
from djmodel.serializers import NouseNameSerializer, NouseUserSerializer
# from djmodel.serializers import StarsSerializer
# from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView  # , ListView
# from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# from rest_framework.parsers import FileUploadParser,
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import CreateAPIView, GenericAPIView,ListAPIView
from pyfcm import FCMNotification
# from rest_framework.authentication import TokenAuthentication
'''from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
'''

# ListAPIView
# from random import randint

import ast
class NotificationView(GenericAPIView):
    parser_classes=(MultiPartParser,FormParser)
    serializer_class=NotificationSerializer
    def post(self,request):
        push_service = FCMNotification(api_key="AAAAnN1TIdw:APA91bGRfLfJJpxML0vtZ2SaQqyr9YHpCuHfbEMRv8NAj0zDK9mNMgUcJL8gEwG4sVVx9Aj0O6fpNfaOQSTHenVTuKxYhhioVNaIzPzVtej98gvq80arWd5M3MoaXiUl4kZSdW2miYuB")
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['deadline']==True:
                message_title=serializer.data['deadline_subject']
                message_body=serializer.data['deadline_topic']
                #registration_id=serializer.data['android_token']
                group_id=serializer.data['group']
                group=Group.objects.filter(group_id=group_id)[0]
                queryset=group.user_set.all()
                registration_id=[]
                for user in queryset:
                    registration_id.append(user.android_token)

                #registration_id="cvmeSxKINBY:APA91bH2U6x7QKsbsaQ40qz8oKyKaN0-7h4xvh2u1654qL4SvMQIMeFXqgADO2RRTJv0mNhwopPZODcPgBPdcwasorRoPBJxlPXboFxO6gCKcpbVmeaFYKElQJgqQMtrhv6CI7duI7qT"
                result = push_service.notify_multiple_devices(registration_ids=registration_id, message_title=message_title, message_body=message_body)
                print(result)
            else:
                message_title=serializer.data['title']
                message_body=serializer.data['body']
                group_id=serializer.data['group']
                group=Group.objects.filter(group_id=group_id)[0]
                queryset=group.user_set.all()
                registration_id=[]
                for user in queryset:
                    registration_id.append(user.android_token)

                #registration_id=serializer.data['android_token']
                #registration_id="cvmeSxKINBY:APA91bH2U6x7QKsbsaQ40qz8oKyKaN0-7h4xvh2u1654qL4SvMQIMeFXqgADO2RRTJv0mNhwopPZODcPgBPdcwasorRoPBJxlPXboFxO6gCKcpbVmeaFYKElQJgqQMtrhv6CI7duI7qT"
                result = push_service.notify_multiple_devices(registration_ids=registration_id, message_title=message_title, message_body=message_body)
                print(result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListNotification(ListAPIView):
    '''Lists all the notifications'''
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginAPIView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializerLogin

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            queryset=Notification.objects.all()
            for notif in queryset:
                if notif.deadline==True:
                    message_title=notif.deadline_subject
                    message_body=notif.deadline_topic
                    registration_id=serializer.data['android_token']
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                    print(result)
                else:
                    message_title=notif.title
                    message_body=notif.body
                    registration_id=serializer.data['android_token']
                    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                    print(result)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


'''
class UserLoginAPIView(APIView):
    def post(self, request, format=None):
            data = request.data

            username = data.get('username', None)
            password = data.get('password', None)

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
'''


class UserLogoutAPIView(APIView):

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class UserRegistrationAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serialized = self.get_serializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


'''
    def post(self, request):
        serialized = UserSerializer(data=data)

        if serialized.is_valid():
            user = User.objects.create(
                username=request.data.get('email'),
                email=request.data.get('email'),
                first_name=request.data.get('firstName'),
                last_name=request.data.get('lastName')
            )
     user.set_password(str(request.data.get('password')))
     user.save()
     return Response({"status":"success","response":"User Successfully Created"}, status=status.HTTP_201_CREATED)
'''


'''def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
'''

# users


class UserView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        List users
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)


# users/{sap_id}
class UserDetail(APIView):
    # authentication_classes = (TokenAuthentication)
    parser_classes = (JSONParser, FormParser)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Delete user
        """

        user = get_object_or_404(User, pk=request.data['sap_id'])
        return Response(UserSerializer(user).data)


class UserDeleteView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        user = get_object_or_404(User, pk=request.data['sap_id'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
    @staticmethod
    def get(request, sap_id):
        """
        View individual user
        """
        # token = Token.objects.filter(user=request.user)
        user = get_object_or_404(User, pk=sap_id)
        return Response(UserSerializer(user).data)
'''
# sap_id = request.data
# user = User.objects.get(sap_id=sap_id)
# user.delete()
# return Response(status=status.HTTP_204_NO_CONTENT)


'''
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
'''


class UserByGroupView(APIView):
    parser_classes = (JSONParser, FormParser)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        print(request)
        print(request.data)
        """
        get all users belonging to group
        """
        groups_ids = ast.literal_eval(request.data['group'])
        user = User.objects.filter(group__in=groups_ids)
        print(user)
        # return Response(UserByGroupSerializer(users).data)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(UserByGroupSerializer(user, many=True).data)


class UserByNameView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        Get all users with same name
        """

        user1 = User.objects.filter(name=request.data['name'])
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
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NouseSerializer

    def post(self, request):
        '''
        Get all files from start_idx to end_idx
        '''
        start_idx = int(request.data['start_idx'])
        end_idx = int(request.data['end_idx'])
        print(isinstance(start_idx, int))
        if request.data['sort_order'] == 'ascending':
            # if sort_by == 'size':
            #     file = File.objects.order_by('size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file, many=True).data)
            if request.data['sort_by'] == 'recent':
                file = File.objects.order_by('time_added')[start_idx - 1:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if request.data['sort_by'] == 'popularity':
                stars = File.objects.order_by('no_of_stars')[start_idx - 1:end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)
        if request.data['sort_order'] == 'descending':
            # if sort_by == 'size':
            #     file = File.objects.order_by('-size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file, many=True).data)
            if request.data['sort_by'] == 'recent':
                file = File.objects.order_by('-time_added')[start_idx - 1:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if request.data['sort_by'] == 'popularity':
                stars = File.objects.order_by('-no_of_stars')[start_idx - 1:end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)


class FileGetByUserView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NouseUserSerializer

    def post(self, request):
        '''
        Get all files of a particular user
        '''
        if 'start_idx' in request.data:
            start_idx = int(request.data['start_idx'])
        else:
            start_idx = 1

        if 'end_idx' in request.data:
            end_idx = int(request.data['end_idx'])
        else:
            end_idx = 10

        if 'sort_by' in request.data:
            sort_by = request.data['sort_by']
        else:
            sort_by = "recent"

        if 'sort_order' in request.data:
            sort_order = request.data['sort_order']
        else:
            sort_order = "descending"

        sap_id = int(request.data['sap_id'])

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
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = NouseNameSerializer

    def post(self, request):
        '''
        Get a file by name
        '''
        start_idx = int(request.data['start_idx'])
        end_idx = int(request.data['end_idx'])
        file_name = request.data['file_name']
        sort_by = request.data['sort_by']
        sort_order = request.data['sort_order']
        if sort_order == 'ascending':
            # if sort_by == 'size':
            #     file = File.objects.get(name=file_name).order_by('size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(name=file_name).order_by('time_added')[start_idx - 1:end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(name=file_name).order_by('no_of_stars')[start_idx - 1:
                                                                                    end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)
        if sort_order == 'descending':
            # if sort_by == 'size':
            #     file = File.objects.get(name=file_name).order_by('-size')[start_idx:end_idx]
            #     return Response(FileOrderingSerializer(file).data)
            if sort_by == 'recent':
                file = File.objects.filter(name=file_name).order_by('-time_added')[start_idx - 1:
                                                                                   end_idx]
                return Response(FileOrderingSerializer(file, many=True).data)
            if sort_by == 'popularity':
                stars = File.objects.filter(name=file_name).order_by('-no_of_stars')[start_idx - 1:
                                                                                     end_idx]
                return Response(FileOrderingSerializer(stars, many=True).data)


class FileGetInfoView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        Get info of a particular file
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        try:
            File.objects.get(file_id=request.data['file_id'])
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(FileGetInfoSerializer(File.objects.get(file_id=request.data['file_id'])).data)


class FileDownloadView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        List users
        """
        # get_data = request.GET.get(['disk_utilization'], ['group'])
        file1 = File.objects.get(file_id=request.data['file_id'])
        return Response(FiledownloadSerializer(file1).data)


class FileDeleteView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        Delete file
        """

        file = get_object_or_404(File, pk=request.data['file_id'])
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class File_PermissionViewSet(viewsets.ModelViewSet):
    queryset = File_Permission.objects.all()
    serializer_class = FilePermissionSerializer


class StarFileView(APIView):
    parser_classes = (JSONParser,)
    serializer_class = FileSerializer

    def post(self, request):
        '''
        Star a file
        '''
        files = get_object_or_404(File, pk=request.data['file_id'])
        files.no_of_stars += 1
        files.save()
        star = Stars.objects.filter(file=files)
        # star.star_id = int(str(file_id) + str(randint(0, 10000)))
        # for i in star:
        #     star.save(['star_id'])
        # print(star.star_id)
        return Response(StarsUpVoteSerializer(star, many=True).data)


class UnStarFileView(APIView):
    parser_classes = (JSONParser,)
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        '''
        Unstar a file
        '''
        files = get_object_or_404(File, pk=request.data['file_id'])
        files.no_of_stars -= 1
        files.save()
        star = Stars.objects.filter(file=files)
        # star.star_id = str(file_id) + str(randint(0, 10000))
        # for i in star:
        #     star.save(['star_id'])
        # print(star)
        return Response(StarsUpVoteSerializer(star, many=True).data)


'''
class FileUploadView(APIView):

    parser_classes = (FileUploadParser,)

    def put(self, request, name, description, format=None):

        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        # extension = file_data.split(".").lower()[-1]
        # print(extension)
        return Response(file_obj.file_id, status.HTTP_201_CREATED)

    def model_form_upload(request):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {
            'form': form
        })
'''


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            push_service = FCMNotification(api_key="AAAAnN1TIdw:APA91bGRfLfJJpxML0vtZ2SaQqyr9YHpCuHfbEMRv8NAj0zDK9mNMgUcJL8gEwG4sVVx9Aj0O6fpNfaOQSTHenVTuKxYhhioVNaIzPzVtej98gvq80arWd5M3MoaXiUl4kZSdW2miYuB")
            message_title='New File Upload'

            user=User.objects.filter(sap_id=file_serializer.data['submitted_by'])[0]
            message_body=str(user.name)+' uploaded '+file_serializer.data['name']
            group=user.group
            registration_ids=[]
            queryset=group.user_set.all()
            for student in queryset:
                registration_ids.append(student.android_token)

            result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
            print(result)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
