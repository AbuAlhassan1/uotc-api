# Generated by Django 4.0.4 on 2022-05-29 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gathering', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gathering',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gathering_leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gatheringentities',
            name='entities',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gatheringrequest',
            name='From',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='From', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gatheringrequest',
            name='to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='to', to=settings.AUTH_USER_MODEL),
        ),
    ]
