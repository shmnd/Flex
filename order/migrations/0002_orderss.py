# Generated by Django 4.2.5 on 2023-11-09 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orderss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_created_at_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
