# Generated by Django 4.0.4 on 2022-04-22 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytoken', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytoken',
            name='token',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
