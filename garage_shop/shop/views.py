from typing import Any
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm, CustomerForm, AddToCartForm, OrderCreateForm
# CustomerEditForm, UserEditForm
from .models import CategoryManager, Customer, Category, Product, Oil, Filter, OrderItem, Order
# from .models import Oil, Filter, Customer, Product, Category, Cart, ProductCart
from django.views.generic import DetailView, View
# from .mixins import CartMixin, NotificationsMixin
from .mixins import CategoryMixin, CategoryLeftMixin, ProductAvailableMixin
# NotificationsMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .cart import Cart




def index(self, request):
    # categories нужна для /product/
    # categories = Category.objects.get_caterories_for_left_sedebar()
    # разобраться со строкой 14 15 16 не понимаю!!!
    categories = Category.objects.all()
    context = {
        'categories': categories,
        # 'notifications': self.notifications(request.user)
    }

    return render(
        request,
        'shop/index.html',
        context
    )


def info_shop(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        # 'notifications': self.notifications(request.user)
    }
    return render(request, 'shop/info_shop.html', context)


# def success(request):
#     email = request.POST.get('email', '')
#     newsletter = request.POST.get('checkbox', '')
#     data = """
# Hello there!
#
# I wanted to personally write an email in order to welcome you to our platform.\
#  We have worked day and night to ensure that you get the best service. I hope \
# that you will continue to use our service. We send out a newsletter once a \
# week. Make sure that you read it. It is usually very informative.
#
# Cheers!
# ~ Yasoob
#     """
#     user = Contact(email=email)
#     user.save()
#     if newsletter == 'on':
#         send_mail('Welcome!', data, "Yasoob",
#                   [email], fail_silently=False)
#     return render(request, 'contact.html')


class ProductDetailView(CategoryLeftMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'

    CT_MODEL_MODEL_CLASS = {
        'oil': Oil,
        'filter': Filter,
    }

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # form = AddToCartForm()
        return super().get(request, *args, **kwargs)

    # встроенная функция во view
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)


# шаблон где рандерится информация о товаре
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['form'] = AddToCartForm()
        return context


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account')
                    # return render(request, 'shop/account.html')
                    # return HttpResponse('Проверка подлинности прошла успешно')
                else:
                    return HttpResponse('Отключенная учетная запись')
            else:
                return HttpResponse('Неверный логин')

        # return render(request, 'shop/account.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['username']
            new_user.email = user_form.cleaned_data['email']
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']
            new_user.save()
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # profile = Profile.objects.create(user=new_user)
            customer = Customer.objects.create(user=new_user,
                                    username=user_form.cleaned_data['username'],
                                    first_name=user_form.cleaned_data['first_name'],
                                    last_name=user_form.cleaned_data['last_name'],
                                    email=user_form.cleaned_data['email'],
                                    phone=user_form.cleaned_data['phone'],
                                    address=user_form.cleaned_data['address'])

            # !!! new_user или user !!!
            user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'shop/info_shop.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': user_form})


# class AccountView(views.View):
#
#     def get(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         context = {
#             'customer': customer,
#             # 'cart': self.cart,
#             # 'notifications': self.notifications(request.user)
#         }
#         return render(request, 'shop/account.html', context)

#
# def register(request):
#     if request.method == 'POST':
#         user_form = RegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             new_user.username = user_form.cleaned_data['username']
#             new_user.email = user_form.cleaned_data['email']
#             new_user.first_name = user_form.cleaned_data['first_name']
#             new_user.last_name = user_form.cleaned_data['last_name']
#             new_user.save()
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             Customer.objects.create(user=new_user,
#                                     phone=user_form.cleaned_data['phone'],
#                                     address=user_form.cleaned_data['address'])
#             user = authenticate(username=user_form.cleaned_data['username'],
#                                 password=user_form.cleaned_data['password'])
#             login(request, user)
#
#             return render(request, 'shop/info_shop.html', {'new_user': new_user})
#     else:
#         user_form = RegistrationForm()
#     return render(request, 'shop/register.html', {'user_form': user_form})

# НАЧАЛО ВАЖНО
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Проверка подлинности прошла успешно')
#                 else:
#                     return HttpResponse('Отключенная учетная запись')
#             else:
#                 return HttpResponse('Неверный логин')
#     else:
#         form = LoginForm()
#     return render(request, 'shop/login.html', {'form': form})
#
#
# def register(request):
#     if request.method == 'POST':
#         user_form = RegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             new_user.username = user_form.cleaned_data['username']
#             new_user.email = user_form.cleaned_data['email']
#             new_user.first_name = user_form.cleaned_data['first_name']
#             new_user.last_name = user_form.cleaned_data['last_name']
#             new_user.save()
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             # profile = Profile.objects.create(user=new_user)
#             # Customer.objects.create(user=new_user,
#             #                         phone=user_form.cleaned_data['phone'],
#             #                         address=user_form.cleaned_data['address'])
#
#             # !!! new_user или user !!!
#             # user = authenticate(username=user_form.cleaned_data['username'],
#             #                         password=user_form.cleaned_data['password'])
#             login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
#
#             return render(request, 'shop/info_shop.html', {'new_user': new_user})
#     else:
#         user_form = RegistrationForm()
#     return render(request, 'shop/register.html', {'form': user_form})
# КОНЕЦ ВАЖНО
# def account(request):
#     return render(request, 'shop/account.html')

class AccountView(views.View):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=request.user)
            form = CustomerForm({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': customer.phone,
                'address': customer.address,
                # 'password': '_',
                # 'confirm_password': '_',
            })
            orders = Order.objects.filter(customer=customer)
            context = {
                'user': user,
                'customer': customer,
                'form': form,
                'orders': orders
            }
            return render(request, 'shop/account.html', context)
        except Exception as ex:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        user_form = CustomerForm(request.POST, instance=request.user)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            customer = Customer.objects.filter(user=request.user)
            customer.update(
                            username=user_form.cleaned_data['username'],
                            first_name=user_form.cleaned_data['first_name'],
                            last_name=user_form.cleaned_data['last_name'],
                            email=user_form.cleaned_data['email'],
                            phone=user_form.cleaned_data['phone'],
                            address=user_form.cleaned_data['address'])
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return render(request, 'shop/account.html', {'form': user})
        return redirect('account')

# @login_required
# def account(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.customer, data=request.POST)
#         profile_form = CustomerEditForm(instance=request.customer, data=request.POST, files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#     else:
#         user_form = UserEditForm(instance=request.customer)
#         profile_form = CustomerEditForm(instance=request.customer)
#         return render(request,
#                       'shop/account.html',
#                       {'user_form': user_form,
#                        'profile_form': profile_form})
#


class CategoryDetailView(CategoryMixin, ProductAvailableMixin, CategoryLeftMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category' # ваше собственное имя переменной контекста в шаблоне
    template_name = 'shop/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get(self, request, *args, **kwargs):
    #     product = Product.objects.filter(available=True)
    #     context = {
    #         'product': product
    #     }
    #     return render(request, '')



    # def get(self, request, *args, **kwargs):
    # # def product_list(self, request, category_slug=None):
    # #     category = Category.objects.all()
    #     products = Product.objects.all()
    #     categories = Category.objects.all()
    # #     # categoria = Category.objects.get_caterories_for_left_sedebar()
    # #     # slug_products = Category.objects.get_absolute_url()
    # #     if category_slug:
    # #         products = products.filter(category=category)
    #     context = {
    #         # 'category': category,
    #         'categories': categories,
    #         'products': products,
    # #         # 'categoria': categoria
    # #         # 'slug_products': slug_products
    # #
    #     }
    #     return render(request, 'shop/category_detail.html', context)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['producst'] = Product.objects.filter(available=True)
    #     context['categories'] = Category.objects.all()
    #     return context
    #     return render('shop/category_detail.html', context)


class ShopDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category' # ваше собственное имя переменной контекста в шаблоне
    template_name = 'shop/product.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'shop/product.html', context)


# для добавления товара в корзину
class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        # cart = Cart.objects.all()
        # # print(kwargs.get('ct_model'))
        # # print(kwargs.get('slug'))
        # ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # customer = Customer.objects.get(user=request.user)
        # cart = Cart.objects.get(guest=customer, id_order=False)
        # content_type = ContentType.objects.get(model=ct_model)
        # product = content_type.model_class().objects.get(slug=product_slug)
        # cart_product, created = ProductCart.objects.get_or_create(
        #     user=cart.guest, cart=cart, content_type=content_type, content_id=product.id, final_price=product.price)
        # cart.products.add(cart_product)
        # if created:
        #     cart.products.add(cart_product)
        # # recalc_cart(self.cart)
        # messages.add_message(request, messages.INFO, "Товар успешно добавлен")

        return HttpResponseRedirect('/cart/')



@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def order_create(request):
    customer = Customer.objects.get(username=request.user)
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if customer is not None:
                order.customer = customer
            order.total_price = cart.get_total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        if customer is not None:
            form = OrderCreateForm({
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone': customer.phone,
                'address': customer.address,
                # 'password': '_',
                # 'confirm_password': '_',
            })
        else:
            form = OrderCreateForm
    return render(request, 'shop/order_create.html', {'cart': cart, 'form': form})

# Выход из личного кабинета
def custom_logout(request):
    logout(request)
    return render(request, 'shop/info_shop.html')


class AboutCompony(DetailView):

    # model = Category
    # queryset = Category.objects.all()
    # context_object_name = 'category'  # ваше собственное имя переменной контекста в шаблоне
    # template_name = 'shop/category_detail.html'
    # slug_url_kwarg = 'slug'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'shop/about_compony.html', context)


class Delivery(DetailView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'shop/delivery.html', context)


class AddressCompony(DetailView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'shop/address_compony.html', context)


