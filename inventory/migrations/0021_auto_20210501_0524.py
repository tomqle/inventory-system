# Generated by Django 3.2 on 2021-05-01 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20210425_0740'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='SalesOrder',
        ),
        migrations.RenameModel(
            old_name='OrderLine',
            new_name='SalesOrderLine',
        ),
    ]
