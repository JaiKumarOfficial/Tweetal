# Generated by Django 2.2.3 on 2019-07-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.TextField(max_length=200)),
                ('document', models.FileField(blank=True, null=True, upload_to='documents/')),
            ],
        ),
    ]
