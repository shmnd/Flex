# Generated by Django 4.2.5 on 2023-09-15 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_alter_category_options_category_is_available_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(max_length=50)),
                ('is_avilable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='price_range',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low', models.IntegerField()),
                ('high', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_chart', models.CharField(max_length=30)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(default='no images', upload_to='media/products')),
                ('image2', models.ImageField(default='no images', upload_to='media/products')),
                ('image3', models.ImageField(default='no images', upload_to='media/products')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_price', models.IntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('product_description', models.TextField(max_length=200)),
                ('is_available', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('sizes', models.ManyToManyField(to='product.size')),
            ],
        ),
    ]
