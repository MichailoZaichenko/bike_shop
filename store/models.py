from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import  cache
from django.core.cache.utils import make_template_fragment_key

class FeedBack(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, verbose_name="Email", blank=True, null=True)
    feedback = models.TextField(max_length=300, verbose_name="Feedback")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created at")

    def save(self, *args, **kwargs):
        self.email = self.user.email
        super().save(*args, **kwargs)


class PayingWay(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, verbose_name='card_number')


    def __str__(self):
        return f"{self.card_number} ({self.user.username})"
    # def __str__(self):
    #     return self.locality

class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return f"{self.city}({self.locality})"


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:all-categories')

    def save(self, *args, **kwargs):
        key = make_template_fragment_key('categorie_list')
        cache.delete(key)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        key = make_template_fragment_key('categorie_list')
        cache.delete(key)

        return super().delete(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(max_length=255, unique=True, verbose_name="Unique Product ID (SKU)")
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product-detail', kwargs={'slug':self.slug})

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)

    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Очікує на розгляд', 'Очікує на розгляд'),
    ('Прийнят', 'Прийнят'),
    ('Упакований', 'Упакований'),
    ('На шляху', 'На шляху'),
    ('Доставлено', 'Доставлено'),
    ('Скасовано', 'Скасовано')
)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    paying_way = models.ForeignKey(PayingWay, verbose_name="Paying Way", on_delete=models.CASCADE, blank=True,
                                   null=True)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Очікує на розгляд"
        )
