from django.contrib import admin
from .models import *

admin.site.register(Shoes)
admin.site.register(Tag)
admin.site.register(SizeShoe)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(CartItem)


