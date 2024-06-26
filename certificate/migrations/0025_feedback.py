# Generated by Django 4.2 on 2024-01-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0024_certificate_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.CharField(max_length=12)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
            ],
        ),
    ]
