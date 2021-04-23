# Generated by Django 3.1.6 on 2021-02-20 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210209_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocation',
            name='qty',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterUniqueTogether(
            name='allocation',
            unique_together={('batch', 'order_line', 'qty')},
        ),
    ]