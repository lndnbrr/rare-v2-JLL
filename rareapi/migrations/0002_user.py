# Generated by Django 4.1.3 on 2025-06-11 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bio', models.CharField(max_length=200)),
                ('profile_image_url', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('is_staff', models.BooleanField()),
                ('uid', models.CharField(max_length=100)),
            ],
        ),
    ]
