from django.contrib import admin
from .models import Recipe, Ingredient, RecipeCategory
# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, ItemAdmin)
admin.site.register(Ingredient, ItemAdmin)
admin.site.register(RecipeCategory, ItemAdmin)
