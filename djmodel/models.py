from django.db import models

from django.conf import settings
import uuid
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
# Create your models here.
# from djmodel.managers import UserManager
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# from djmodel import constants
from vote.models import VoteModel


# Create your models here.
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


'''class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.sap_id
'''


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        default_related_name = 'reset_password_codes'

    def __str__(self):
        return f'{self.user.sap_id} - {self.code}'


class Group(models.Model):
    division = models.CharField(max_length=1)
    year = models.IntegerField()
    group_id = models.BigIntegerField(primary_key=True)
    total_disk_available = models.FloatField()
    category = (("S", "Student"), ("T", "Teacher"), )
    category = models.CharField(max_length=1, choices=category, default="S",
                                null=False)

    class Meta:
        ordering = ['category', 'year']


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    bio = models.TextField()
    name = models.CharField(max_length=100)

    # password = models.CharField(_('password'),max_length=50, default="", null=False)
    sap_id = models.BigIntegerField(primary_key=True,
                                    validators=[MaxValueValidator(99999999999),
                                                MinValueValidator(10000000000)])
    disk_utilization = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
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


class File(VoteModel, models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=100)
    file_id = models.BigIntegerField(primary_key=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField()
    no_of_downloads = models.IntegerField()

    # no_of_stars = models.IntegerField(choices=constants.VOTE_VALUE_CHOICES)
    file_data = models.FileField(upload_to=None, max_length=100)
    description = models.TextField(default='')

    class Meta:
        ordering = ['size', 'time_added']

    no_of_stars = models.IntegerField()
    file_data = models.BinaryField()

    class Meta:
        ordering = ['size']



class File_Permission(models.Model):
    permission_id = models.BigIntegerField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(Group, on_delete=models.CASCADE)


class Stars(models.Model):
    star_id = models.BigIntegerField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    starred_by = models.ForeignKey(User, on_delete=models.CASCADE)
