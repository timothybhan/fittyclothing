# Generated by Django 2.2.15 on 2020-08-21 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200820_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]
