from django.db import models

# Create your models here.
# Create your models here.
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())



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
    password = models.CharField(max_length=100, default="", null=False)
    sap_id = models.BigIntegerField(primary_key=True)
    disk_utilization = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created', ]


class File(models.Model):
    time_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=100)
    file_id = models.BigIntegerField(primary_key=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField()
    no_of_downloads = models.IntegerField()
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
