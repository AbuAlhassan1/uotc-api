# Generated by Django 4.0.4 on 2022-04-23 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_myuser_premition_level_alter_myuser_role_hob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='premition_level',
            field=models.IntegerField(default=1, max_length=1),
        ),
    ]