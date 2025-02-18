from django.contrib import admin
from Orders.models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderContent)
admin.site.register(OrderHeader)
admin.site.register(CompleteOrder)