# Generated by Django 3.1.6 on 2021-04-11 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20210404_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='reception',
            name='qty',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
