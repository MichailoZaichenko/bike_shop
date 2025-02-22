# Generated by Django 4.1.7 on 2023-04-02 12:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_order_status_payingway'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email'),
        ),
    ]
