# Create your models here.
from django.db import models


class User(models.Model):
    id = models.IntegerField
    Username = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=500, null=False)
    Confirm_password = models.CharField(max_length=500, null=False)
    # image = models.ImageField(upload_to="uploads", null=True, blank=True)
    # user_type = models.CharField(max_length=100)
    #
    class Meta:
        db_table = "users_tbl"
