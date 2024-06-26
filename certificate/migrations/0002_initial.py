# Generated by Django 4.2 on 2023-09-25 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='certificate_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='holder_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.clientaddress'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.manufacturer'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='manufacturer_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.manufactureraddress'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='product_standard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificate.standards'),
        ),
    ]
