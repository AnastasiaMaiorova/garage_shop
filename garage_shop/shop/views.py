from django.http import HttpResponse
from django import views
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
from .models import Customer
from .models import Oil, Filter, Customer, Product, Category
from django.views.generic import DetailView, View


def index(request):
    # categories = Category.objects.get_caterories_for_left_sedebar()
    # context = {
    #     'products': products,
    # }
    return render(
        request,
        'shop/index.html',
    )

def info_shop(request):
    return render(request, 'shop/info_shop.html', {})

class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'oil': Oil,
        'filter': Filter
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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
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
                                    phone=user_form.cleaned_data['phone'],
                                    address=user_form.cleaned_data['address'])
            # !!! new_user или user !!!
            new_user = authenticate(email=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password'])

            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': user_form})

