# Generated by Django 4.2 on 2023-10-03 02:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standards',
            old_name='standard_title',
            new_name='standard',
        ),
        migrations.RemoveField(
            model_name='standards',
            name='standard_code',
        ),
        migrations.AddField(
            model_name='standards',
            name='remark',
            field=models.TextField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standards',
            name='standard_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standards',
            name='standard_number',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standards',
            name='year',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
