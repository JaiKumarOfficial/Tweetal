# Generated by Django 2.2.3 on 2019-07-24 06:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet',
            field=models.TextField(default='tweet me !!', max_length=200),
        ),
    ]
