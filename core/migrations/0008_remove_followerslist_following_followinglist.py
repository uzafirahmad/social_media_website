# Generated by Django 4.0.1 on 2022-09-23 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_followerslist_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followerslist',
            name='following',
        ),
        migrations.CreateModel(
            name='followinglist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('following', models.CharField(default='', max_length=10000)),
                ('fuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
