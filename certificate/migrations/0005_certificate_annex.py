# Generated by Django 4.2 on 2023-10-05 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0004_alter_standards_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='annex',
            field=models.TextField(blank=True),
        ),
    ]
