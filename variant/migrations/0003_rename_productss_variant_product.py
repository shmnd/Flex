# Generated by Django 4.2.5 on 2023-09-20 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variant', '0002_rename_product_variant_productss'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='productss',
            new_name='product',
        ),
    ]