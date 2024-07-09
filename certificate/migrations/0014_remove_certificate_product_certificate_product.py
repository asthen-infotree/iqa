# Generated by Django 4.2 on 2023-12-15 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0013_remove_certificate_additional_information_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='product',
        ),
        migrations.AddField(
            model_name='certificate',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='certificate.product'),
        ),
    ]