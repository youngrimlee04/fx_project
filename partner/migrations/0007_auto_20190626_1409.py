# Generated by Django 2.2.1 on 2019-06-26 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20190626_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.FloatField(verbose_name='통화 단위당 가격'),
        ),
    ]
