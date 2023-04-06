import django
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from store.models import Address, Cart, Category, Order, Product, FeedBack, PayingWay
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm, FeedbackForm, PayingWayForm
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
        'your_account': your_account,
    }
    return render(request, 'store/index.html', context)


def main(request):
    your_account = request.user
    context = {'your_account': your_account, }
    return render(request, 'store/main.html', context)


def contacts(request):
    your_account = request.user
    context = {'your_account': your_account, }
    return render(request, 'store/contacts.html', context)


def about(request):
    your_account = request.user
    context = {'your_account': your_account, }
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
    return render(request, 'store/categories.html', {'categories': categories, "your_account": request.user})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)

    if request.method == 'POST':
        sort_order = request.POST.get('sort_order')
        if sort_order == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_order == 'price_high_to_low':
            products = products.order_by('-price')
        elif sort_order == 'defalt':
            products = products.order_by('id')
    else:
        products = products.order_by('id')

    categories = Category.objects.filter(is_active=True)
    count_of_products = Product.objects.all().count()
    your_account = request.user
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'count_of_products': count_of_products,
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
            messages.success(request, "Щиро вітаю! Реєстрація успішна! Натисніть кнопку увійти, щоб зайти в акаунт!")
            form.save()
        # return render(request, 'account/register.html', {'form': form})
        # return redirect('store:login')
        return render(request, 'account/register.html', {'form': form})

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    paying_ways = PayingWay.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    your_account = request.user
    return render(request, 'account/profile.html', {'addresses': addresses, 'orders': orders, 'your_account':
        your_account, 'paying_ways': paying_ways})


@method_decorator(login_required, name='dispatch')
class FeedbackView(View):

    def get(self, request):
        email = request.user.email
        your_account = request.user
        form = FeedbackForm()
        return render(request, 'store/contacts.html', {'form': form, 'your_account': your_account, 'email': email})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            user = request.user
            feedback = form.cleaned_data['feedback']
            reg = FeedBack(user=user, feedback=feedback, created_at=timezone.now())
            reg.save()

            # Todo Отправка письма на email пользователя
            # subject = 'Ваш відгук успішно надіслано'
            # message = 'Доброго дня! Ваш відгук успішно надіслано.'
            # from_email = 'michailo.zaichenko@gmail.com'  # Укажите ваш email
            # recipient_list = [email]
            # send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Вітаємо відгук надіслано успішно")
            return redirect('store:profile')
        else:
            your_account = request.user
            return render(request, 'store/contacts.html', {'form': form, 'your_account': your_account, })


@method_decorator(login_required, name='dispatch')
class PayingWayView(View):
    def get(self, request):
        your_account = request.user
        form = PayingWayForm()
        return render(request, 'account/add_paying_way.html', {'form': form, 'your_account': your_account, })

    def post(self, request):
        form = PayingWayForm(request.POST)
        if form.is_valid():
            user = request.user
            card_number = form.cleaned_data['card_number']
            CVV = form.cleaned_data['CVV']
            reg = PayingWay(user=user, card_number=card_number, CVV=CVV)
            reg.save()
            messages.success(request, "Нова картка додана успішно")
            return redirect('store:profile')
        else:
            your_account = request.user
            return render(request, 'account/add_paying_way.html', {'form': form, 'your_account': your_account, })


@login_required
def remove_payingway(request, id):
    a = get_object_or_404(PayingWay, user=request.user, id=id)
    a.delete()
    messages.success(request, "Картка прибрана!")
    return redirect('store:profile')


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        your_account = request.user
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form, 'your_account': your_account, })

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, locality=locality, city=city, state=state)
            reg.save()
            messages.success(request, "Нову адресу успішно додано")
            return redirect('store:profile')
        else:
            your_account = request.user
            return render(request, 'account/add_address.html', {'form': form, 'your_account': your_account, })


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
    cp = [p for p in Cart.objects.all() if p.user == user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    addresses = Address.objects.filter(user=user)
    paying_ways = PayingWay.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'paying_ways': paying_ways,
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
    email = request.user.email
    addresses = Address.objects.filter(user=request.user)
    paying_ways = PayingWay.objects.filter(user=user)
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

    context = {
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
        'your_account': your_account,
        'email': email,
        'addresses': addresses,
        'paying_ways': paying_ways,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    your_account = request.user
    return render(request, 'store/orders.html', {'orders': orders, 'your_account': your_account, })


def custom_handler_404(request, exception):
    return render(request, '404.html', status=404)


def test(request):
    return render(request, 'store/test.html')
