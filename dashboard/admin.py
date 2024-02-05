from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ShopType)
admin.site.register(Category)
admin.site.register(Icon)
admin.site.register(Shop)
# admin.site.register(ShopCategory)


