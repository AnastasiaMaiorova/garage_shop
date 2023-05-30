# Generated by Django 4.1.4 on 2023-05-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Новый заказ', 'Новый заказ'), ('cancelled', 'Заказ отменен'), ('in_progress', 'Заказ в обработке'), ('is_ready', 'Заказ готов'), ('completed', 'Заказ получен покупателем')], default='Новый заказ', max_length=100, verbose_name='Статус заказа'),
        ),
    ]