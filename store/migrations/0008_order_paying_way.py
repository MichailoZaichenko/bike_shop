# Generated by Django 4.1.7 on 2023-04-03 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_feedback_created_at_alter_feedback_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paying_way',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.payingway', verbose_name='Paying Way'),
        ),
    ]
