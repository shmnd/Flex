# Generated by Django 4.2.5 on 2023-09-20 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variant', '0003_rename_productss_variant_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='pricerange',
        ),
    ]