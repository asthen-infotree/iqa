# Generated by Django 4.2 on 2023-11-28 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0008_alter_productdescription_additional_info_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='product_name',
        ),
    ]
