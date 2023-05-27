from django.contrib import admin
from .models import Address, Category, Product, Cart, Order, FeedBack, PayingWay
from modeltranslation.admin import TranslationAdmin
# Register your models here.

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')

class PayingWayAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'CVV')
    list_per_page = 10
    search_fields = ('card_number', 'CVV')

class CategoryAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}


class ProductAdmin(TranslationAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category', 'short_description')
    prepopulated_fields = {"slug": ("title", )}

class CartAdmin(TranslationAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user', 'product')


class OrderAdmin(TranslationAdmin):
    list_display = ('user', 'product', "address", 'quantity', 'status', 'ordered_date')
    list_editable = ('status',)
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user', 'product')

class FeedbeckAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', "email", 'feedback')
    list_editable = ("email",'feedback',)
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