from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Cart, Order
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'detail_description', 'category')

@register(Cart)
class CartTranslationOptions(TranslationOptions):
    fields = ('product',)

@register(Order)
class OrderTranslationOptions(TranslationOptions):
    fields = ('address', 'product', 'status')