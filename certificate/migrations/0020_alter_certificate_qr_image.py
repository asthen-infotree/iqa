# Generated by Django 4.2 on 2023-12-20 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0019_certificate_qr_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='qr_image',
            field=models.ImageField(blank=True, null=True, upload_to='QRCode/'),
        ),
    ]
