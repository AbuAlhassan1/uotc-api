# Generated by Django 4.0.4 on 2022-04-21 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
