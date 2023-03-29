import django
from django.contrib.auth.models import User
from store.models import Address, Cart, Category, Order, Product, FeedBack
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm, FeedbackForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:6]
    products = Product.objects.filter(is_active=True, is_featured=True)[:12]
    your_account = request.user
    context = {
        'categories': categories,
        'products': products,
        'your_account':your_account,
    }
    return render(request, 'store/index.html', context)

def main(request):
    your_account = request.user
    context = {'your_account':your_account,}
    return render(request, 'store/main.html', context)

def contacts(request):
    your_account = request.user
    context = {'your_account':your_account,}
    return render(request, 'store/contacts.html', context)

def about(request):
    your_account = request.user
    context = {'your_account':your_account,}
    return render(request, 'store/about.html', context)

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # your_account = request.user
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,
        # 'your_account': your_account,
    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    your_account = request.user
    return render(request, 'store/categories.html', {'categories':categories, "your_account":request.user})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    count_of_products = Product.objects.all().count()
    your_account = request.user
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'count_of_products':count_of_products,
        'your_account': your_account,
    }
    return render(request, 'store/category_products.html', context)


# Registration

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Щиро вітаю! Реєстрація успішна!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    your_account = request.user
    return render(request, 'account/profile.html', {'addresses':addresses, 'orders':orders, 'your_account': your_account,})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        your_account = request.user
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form, 'your_account': your_account,})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "Новый адрес успешно добавлен.")
        return redirect('store:profile')

@method_decorator(login_required, name='dispatch')
class FeedbackView(View):

    def get(self, request):
        your_account = request.user
        form = FeedbackForm()
        return render(request, 'store/contacts.html', {'form': form, 'your_account': your_account,})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']
            feedback = form.cleaned_data['feedback']
            reg = FeedBack(user=user, email=email, feedback=feedback)
            reg.save()
            messages.success(request, "Вітаємо відгук надіслано успішно")
        return redirect('store:profile')

@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Адрес прибран!")
    return redirect('store:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    your_account = request.user
    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('store:cart')


@login_required
def cart(request):
    your_account = request.user
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    # Display Total on Cart Page
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'your_account': your_account,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Товар видалено з кошика.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    user = request.user
    your_account = request.user
    address_id = request.GET.get('address')

    address = get_object_or_404(Address, id=address_id)
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address, product=c.product, quantity=c.quantity).save()
        # And Deleting from Cart
        c.delete()
    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    # using list comprehension to calculate total amount based on quantity and shipping
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    # Customer Addresses
    addresses = Address.objects.filter(user=user)

    context = {
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'your_account': your_account,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    your_account = request.user
    return render(request, 'store/orders.html', {'orders': all_orders, 'your_account': your_account,})


def custom_handler_404(request, exception):
    return render(request, '404.html', status=404)





def test(request):
    return render(request, 'store/test.html')
