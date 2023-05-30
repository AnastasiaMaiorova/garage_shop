from django.shortcuts import render
from django.core.mail import send_mail
from .models import MailModel

# Create your views here.
def success(request):
    email = request.POST.get('email', '')
    print([email])
    theme = "Тема"
    data = "Текст"
    send_mail(
        subject=theme, 
        message=data, 
        from_email=None,
        recipient_list=[email], 
        fail_silently=False)
    if MailModel.objects.filter(email=email) is not None:
        MailModel.objects.create(email=email)
    return render(request, 'shop/info_shop.html')