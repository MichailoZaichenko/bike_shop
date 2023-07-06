from django.contrib import admin
from .models import Address, Category, Product, Cart, Order, FeedBack, PayingWay

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')

class PayingWayAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number')
    list_per_page = 10
    search_fields = ('card_number',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}

class Product_Resurse(resources.ModelResource):
    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(Category, 'title'))
    class Meta:
        model = Product

class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = Product_Resurse
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
#     list_editable = ('category', 'is_active', 'is_featured')
#     list_filter = ('category', 'is_active', 'is_featured')
#     list_per_page = 10
#     search_fields = ('title', 'category', 'short_description')
#     prepopulated_fields = {"slug": ("title", )}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', "address", 'quantity', 'status', 'ordered_date')
    list_editable = ('status',)
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')

class FeedbeckAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', "email", 'feedback')
    list_filter = ("created_at",)
    list_per_page = 20
    search_fields = ('user', 'created_at', "email", 'feedback')

admin.site.register(Address, AddressAdmin)
admin.site.register(PayingWay, PayingWayAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(FeedBack, FeedbeckAdmin)