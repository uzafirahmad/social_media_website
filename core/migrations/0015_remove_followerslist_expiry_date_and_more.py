# Generated by Django 4.0.1 on 2022-10-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_followerslist_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followerslist',
            name='expiry_date',
        ),
        migrations.AddField(
            model_name='accounts',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
