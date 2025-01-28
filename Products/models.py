from django.db import models

# Create your models here.
class Products (models.Model):
    name = models.CharField(max_length=60)
    family = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.family} - {self.name}'
class Family (models.Model):
    family = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.family}'

class Reason (models.Model):
    reason = models.CharField(max_length=60)
    family = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.family} - {self.reason}'

class Status (models.Model):
    status = models.CharField(max_length=30)
    family = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.family} - {self.status}'

class Cig (models.Model):
    cig = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.cig}'
    