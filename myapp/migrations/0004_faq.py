# Generated by Django 5.1.7 on 2025-04-19 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_userprofile_location_userprofile_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=1024)),
                ('question', models.TextField()),
            ],
        ),
    ]
