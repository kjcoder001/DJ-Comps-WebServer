from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from djmodel import views
from django.urls import path

# from djmodel.views import LoginView, LogoutView, UserView, UserDetail


router = DefaultRouter()
router.register(r'Group', views.GroupViewSet)
# router.register(r'File', views.FileViewSet)
router.register(r'File_Permission', views.File_PermissionViewSet)
# router.register(r'Stars', views.StarsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login$', views.UserLoginAPIView.as_view()),
    url(r'^logout$', views.UserLogoutAPIView.as_view()),
    url(r'^register$', views.UserRegistrationAPIView.as_view()),
    url(r'^users$', views.UserView.as_view()),
    # url(r'^users/(?=.{5,11}$)(?P<sap_id>[0-9]+)$', views.UserDetail.as_view()),
    url(r'^users/sap_id$', views.UserDetail.as_view()),
    # url(r'^users/(?P<name>[A-Za-z]+)$', views.UserByNameView.as_view()),
    url(r'^users/name$', views.UserByNameView.as_view()),
    url(r'^users/delete$', views.UserDeleteView.as_view()),


    # url(r'^users/(?=.{1,4}$)(?P<group>[\d]+)$', views.UserByGroupView.as_view()),
    url(r'^users/group$', views.UserByGroupView.as_view()),

    url(r'^users/get-disk-utilization$', views.UserDiskUtilizationView.as_view()),
    # url(r'^file/get-all$', views.FileGetAllView.as_view()),
    # path('file/<int:start_idx>/<int:end_idx>/<slug:sort_by>/<slug:sort_order>/',
    #      views.FileGetAllView.as_view()),
    path('file/get-all', views.FileGetAllView.as_view()),

    # path('file/user=<slug:sap_id>/<int:start_idx>/<int:end_idx>/<slug:sort_by>/<slug:sort_order>/',
    #      views.FileGetByUserView.as_view()),
    path('file/user', views.FileGetByUserView.as_view()),

    # path('file/filename=<slug:file_name>/<int:start_idx>/<int:end_idx>/<slug:sort_by>/<slug:sort_order>/',
    #     views.FileGetByNameView.as_view()),
    path('file/name', views.FileGetByNameView.as_view()),

    # path('file/fileid=<int:file_id>/', views.FileGetInfoView.as_view()),
    path('file/getinfo', views.FileGetInfoView.as_view()),

    # path('file/download/<int:file_id>/', views.FileDownloadView.as_view()),
    path('file/download', views.FileDownloadView.as_view()),

    # path('file/delete/fileid=<int:file_id>/', views.FileDeleteView.as_view()),
    path('file/delete', views.FileDeleteView.as_view()),
    path('star/star-file', views.StarFileView.as_view()),
    path('star/unstar-file', views.UnStarFileView.as_view()),
    url(r'^file/upload/$', views.FileUploadView.as_view()),
    # path('file/upload/<slug:name>/<slug:description>/<slug:file_data>/',
    #       views.FileUploadView.as_view()),
]
