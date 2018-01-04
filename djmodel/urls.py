from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from djmodel import views


router = DefaultRouter()
router.register(r'User', views.UserViewSet)
router.register(r'Group', views.GroupViewSet)
router.register(r'File', views.FileViewSet)
router.register(r'File_Permission', views.File_PermissionViewSet)
router.register(r'Stars', views.StarsViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
