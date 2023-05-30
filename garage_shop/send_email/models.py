from django.db import models

class MailModel(models.Model):
    email = models.EmailField(max_length=255, verbose_name='Почта')

    class Meta:
        verbose_name = 'Почта для подписки'
        verbose_name_plural = 'Почты для подписки'
