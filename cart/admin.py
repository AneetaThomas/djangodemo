from django.contrib import admin
from cart.models import Cart,Payment,Order_details
# Register your models here.
admin.site.register(Cart),
admin.site.register(Payment),
admin.site.register(Order_details)
