# Generated by Django 3.2 on 2021-05-01 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20210501_0524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allocation',
            old_name='order_line',
            new_name='sales_order_line',
        ),
        migrations.RenameField(
            model_name='batch',
            old_name='order_lines',
            new_name='sales_order_lines',
        ),
        migrations.RenameField(
            model_name='salesorderline',
            old_name='order',
            new_name='sales_order',
        ),
        migrations.AlterUniqueTogether(
            name='allocation',
            unique_together={('batch', 'sales_order_line', 'qty')},
        ),
    ]