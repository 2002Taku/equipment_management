from django.contrib import admin
from .models import Equipment, Item, Category, Tag

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('category',)

admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Tag)