# Generated by Django 4.2.5 on 2023-09-22 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wishlist_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='varinat',
            new_name='variant',
        ),
    ]
