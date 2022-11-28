from django.contrib import admin
from .models import Product, Category, Client, Order


def add_stock(ModelAdmin, request, queryset):
    for obj in queryset:
        obj.stock = obj.stock +50
        obj.save()
    # queryset.update(restocked = True)
    return


add_stock.short_description = 'Restock'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [add_stock]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'get_interested_in')


# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
