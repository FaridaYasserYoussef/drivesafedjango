# Generated by Django 5.0.3 on 2024-04-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_driver_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='password',
            field=models.CharField(default='', max_length=64),
        ),
    ]
