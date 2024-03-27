# Generated by Django 4.2 on 2024-03-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0029_alter_certificate_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='template',
            field=models.CharField(choices=[('1', 'TEMPLATE 1'), ('2', 'TEMPLATE 2'), ('3', 'TEMPLATE 3'), ('4', 'TEMPLATE 4')], default='1', max_length=1),
        ),
    ]
