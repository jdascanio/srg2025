from django.db import models
from django.contrib.auth.models import User

# Create your models here..
class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_nr = models.CharField(max_length=10, null=True, blank=True)

class OrderHeader (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10)
    user_name = models.CharField(max_length=20)
    total_products = models.IntegerField()
    tracking = models.CharField(max_length=40, null=True, blank=True)
    send_date = models.DateField(null=True, blank=True)
    reception_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    order_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user_name} - {self.order_number}'

class OrderContent (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE, max_length=10, null=True, blank=True)
    prov_order_number = models.CharField(max_length=20)
    family = models.CharField(max_length=20)
    status = models.CharField(max_length=30, null=True, blank=True)
    missing_elem = models.CharField(max_length=40, null=True, blank=True)
    product = models.CharField(max_length=60)
    in_sn = models.CharField(max_length=20, null=True, blank=True)
    client = models.CharField(max_length=30, null=True, blank=True)
    seller = models.CharField(max_length=30, null=True, blank=True)
    reason = models.CharField(max_length=60)
    cig = models.CharField(max_length=6, null=True, blank=True)
    observations = models.CharField(max_length=200, null=True, blank=True)
    out_sn = models.CharField(max_length=20, null=True, blank=True)
    invoice = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user_name} - {self.order_number}'