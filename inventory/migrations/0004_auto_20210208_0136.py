# Generated by Django 3.1.6 on 2021-02-08 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210208_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocation',
            name='date_allocated',
            field=models.DateField(default=datetime.datetime(2021, 2, 8, 1, 36, 11, 562937)),
        ),
        migrations.AlterField(
            model_name='batch',
            name='eta',
            field=models.DateField(blank=True, null=True),
        ),
    ]
