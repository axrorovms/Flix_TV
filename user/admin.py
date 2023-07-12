from django.contrib import admin
from user.models.user_ import User
from user.models.wishlist import Wishlist


admin.site.register(User)
admin.site.register(Wishlist)