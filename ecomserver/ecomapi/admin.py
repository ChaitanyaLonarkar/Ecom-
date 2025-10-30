from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Address)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(OrderItem)
admin.site.register(Notification)
admin.site.register(Discount)
admin.site.register(Coupon)
admin.site.register(CartItem)

