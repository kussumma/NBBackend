# Generated by Django 4.2.1 on 2023-05-26 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_rating_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='color',
        ),
    ]
