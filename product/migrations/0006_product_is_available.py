# Generated by Django 4.2.5 on 2023-09-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_remove_product_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
