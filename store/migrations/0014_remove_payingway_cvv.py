# Generated by Django 3.2.3 on 2023-06-05 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20230529_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payingway',
            name='CVV',
        ),
    ]
