from django.contrib import admin
from .models import Item

# this imports your model into the admin interface


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
