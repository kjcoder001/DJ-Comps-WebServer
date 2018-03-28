from django.db import models
from django.conf import settings
import uuid
import os
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
# Create your models here.
# from djmodel.managers import UserManager
# from djmodel import constants
# from vote.models import VoteModel


'''class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.sap_id
'''

class Group(models.Model):
    division = models.CharField(max_length=1)
    year = models.IntegerField()
    group_id = models.BigIntegerField(primary_key=True,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(9999)])
    total_disk_available = models.FloatField()
    category = (("S", "Student"), ("T", "Teacher"), )
    category = models.CharField(max_length=1, choices=category, default="S",
                                null=False)

    class Meta:
        ordering = ['category', 'year']


class Notification(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,blank=True,null=True)
    title=models.CharField(max_length=120,blank=True,null=True,default='')
    body=models.CharField(max_length=120,blank=True,null=True,default='')
    deadline=models.BooleanField(default=False)
    deadline_subject=models.CharField(max_length=120,default='',blank=True,null=True)
    deadline_topic=models.CharField(max_length=120,default='',blank=True,null=True)


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        default_related_name = 'reset_password_codes'

    def __str__(self):
        return f'{self.user.sap_id} - {self.code}'



class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    bio = models.TextField()
    android_token=models.CharField(max_length=200)
    name = models.CharField(max_length=100)

    # password = models.CharField(_('password'),max_length=50, default="", null=False)
    sap_id = models.BigIntegerField(primary_key=True,
                                    validators=[MaxValueValidator(99999999999),
                                                MinValueValidator(10000000000)])
    disk_utilization = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    password = models.CharField(max_length=30, default='')
    confirm_password = models.CharField(max_length=30, default='')


'''
    objects = UserManager()

    USERNAME_FIELD = 'sap_id'

    password = models.CharField(max_length=100, default="", null=False)
    sap_id = models.BigIntegerField(primary_key=True)
    disk_utilization = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


    class Meta:
        ordering = ['created', ]


    def save(self, *args, **kwargs):
        if not self.password:
            self.password = str(uuid.uuid4()).replace('-', '')
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.sap_id

    def get_name(self):
        return self.name
'''


# class File(VoteModel, models.Model):
class File(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    # type1 = models.CharField(max_length=100)
    file_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_downloads = models.IntegerField(default=0)
    no_of_stars = models.IntegerField(default=0)
    file_data = models.FileField(blank=False, null=False)
    description = models.TextField(default='')

    def extension(self):
        name, type1 = os.path.splitext(self.file_data.name)
        return type1

    # class Meta:
    #     ordering = ['time_added']


class File_Permission(models.Model):
    permission_id = models.BigIntegerField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(Group, on_delete=models.CASCADE)


class Stars(models.Model):
    star_id = models.BigIntegerField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    starred_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Tp(models.Model):
    start_idx = models.IntegerField(default=0)
    end_idx = models.IntegerField(default=0)
    category = (("ascending", "ascending"), ("descending", "descending"), )
    sort_order = models.CharField(max_length=10, choices=category, default=None,
                                  null=True)
    category = (("recent", "recent"), ("popularity", "popularity"), )
    sort_by = models.CharField(max_length=10, choices=category, default=None,
                               null=True)
