from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django import views
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
    # UserEditForm, CustomerEditForm
from .models import *
# from .models import Oil, Filter, Customer, Product, Category, Cart, ProductCart
from django.views.generic import DetailView, View

from django.contrib import messages



def index(self, request):
    # categories нужна для /product/
    # categories = Category.objects.get_caterories_for_left_sedebar()
    # разобраться со строкой 14 15 16 не понимаю!!!
    context = {
        # 'categories': categories,
        # 'notifications': self.notifications(request.user)
    }

    return render(
        request,
        'shop/index.html',
        context
    )


def info_shop(request):
    return render(request, 'shop/info_shop.html', {})


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'oil': Oil,
        'filter': Filter,
    }

    # встроенная функция во view
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'

# шаблон где рандерится информация о товаре
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        # context['cart'] = self.cart
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
                    return HttpResponse('Проверка подлинности прошла успешно')
                else:
                    return HttpResponse('Отключенная учетная запись')
            else:
                return HttpResponse('Неверный логин')
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
            Customer.objects.create(user=new_user,
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

# @login_required
# def account(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         profile_form = CustomerEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = CustomerEditForm(instance=request.user.profile)
#         return render(request,
#                       'shop/account.html',
#                       {'user_form': user_form,
#                        'profile_form': profile_form})


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category' # ваше собственное имя переменной контекста в шаблоне
    template_name = 'shop/category_detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        # categories = Category.objects.get_categories_for_left_sidebar()
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        # categoria = Category.objects.get_caterories_for_left_sedebar()
        # slug_products = Product.objects.get_absolute_url()
        context = {
            'categories': categories,
            'products': products,

            # 'categoria': categoria
            # 'slug_products': slug_products

        }
        return render(request, 'shop/category_detail.html', context)


# def oils(request):
#     data = Oil.objects.all()
#     return render(request, 'shop/oils.html', {'data': data})

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



class CartView(View):

    def get(self, request, *args, **kwargs):
        # customer = Customer.objects.get(user=request.user)
        categories = Category.objects.all()
        cart = Cart.objects.all()
        context = {
            # 'customer': customer,
            'categories': categories,
            'cart': cart
        }

        return render(request, 'shop/cart.html', context)


