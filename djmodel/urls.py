from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from djmodel import views

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
    url(r'^users/(?P<sap_id>[\d]+)$', views.UserDetail.as_view()),
    url(r'^users/(?P<name>[\d]+)$', views.UserByNameView.as_view()),
    url(r'^users/(?P<group>[\d]+)$', views.UserByGroupView.as_view()),
    url(r'^users/get-disk-utilization$', views.UserDiskUtilizationView.as_view()),
    url(r'^file/get-all$', views.FileGetAllView.as_view()),
    url(r'^file/(?P<user>[\d]+)$', views.FileGetByUserView.as_view()),
    url(r'^file/(?P<filename>[\d]+)$', views.FileGetByNameView.as_view()),
    url(r'^file/get-info$', views.FileGetInfoView.as_view()),
    url(r'^file/download$', views.FileDownloadView.as_view()),
    url(r'^file/delete$', views.FileDeleteView.as_view()),
    url(r'^star/star-file$', views.StarFileView.as_view()),
    url(r'^star/unstar-file$', views.UnStarFileView.as_view()),
    url(r'^file/upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
]
