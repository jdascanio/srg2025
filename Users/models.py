from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_name = models.CharField(max_length=30)
    passwrd = models.CharField(max_length=40)
    email = models.EmailField(max_length=120)
    distributor = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}-{self.user_name}'